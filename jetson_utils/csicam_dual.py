import cv2
import threading
import numpy as np

def cv2_video_writer(w, h, filename='output.mov'):
    # camera init
    fps = 10 # int(cap.get(cv2.CAP_PR
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    vid_writer = cv2.VideoWriter(filename, fourcc, fps, (w, h))
    return vid_writer



class CSI_Camera:

    def __init__(self):
        # Initialize instance variables
        # OpenCV video capture element
        self.video_capture = None
        # The last captured image from the camera
        self.frame = None
        self.grabbed = False
        # The thread where the video capture runs
        self.read_thread = None
        self.read_lock = threading.Lock()
        self.running = False

    def open(self, gstreamer_pipeline_string):
        self.video_capture = cv2.VideoCapture(
            gstreamer_pipeline_string, cv2.CAP_GSTREAMER
        )
        # Grab the first frame to start the video capturing
        self.grabbed, self.frame = self.video_capture.read()

    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None
        # create a thread to read the camera image
        if self.video_capture != None:
            self.running = True
            self.read_thread = threading.Thread(target=self.updateCamera)
            self.read_thread.start()
        return self

    def stop(self):
        self.running = False
        self.video_capture = None
        # Kill the thread
        self.read_thread.join()
        self.read_thread = None
        self.video_capture.release()
        
    def updateCamera(self):
        # This is the thread to read images from the camera
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frame = frame
            except RuntimeError:
                print("Could not read image from camera")
        # FIX ME - stop and cleanup thread
        # Something bad happened

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame
        

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080
"""


def gstreamer_pipeline(sensor_id, hyp):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            hyp['capture_width'],
            hyp['capture_height'],
            hyp['framerate'],
            hyp['flip_method'],
            hyp['display_width'],
            hyp['display_height'],
        )
    )


def run_dual_csicam(hyp, client=None, plot=None):
    #W=1280
    #H=720
    #rvid = cv2_video_writer(W, H, filename='right.mp4')
    #lvid = cv2_video_writer(W, H, filename='left.mp4')

    window_title = "Dual CSI Cameras"
    left_camera = CSI_Camera()
    left_camera.open(gstreamer_pipeline(sensor_id=0, hyp=hyp))
    left_camera.start()

    right_camera = CSI_Camera()
    right_camera.open(gstreamer_pipeline(sensor_id=1, hyp=hyp))
    right_camera.start()

    if left_camera.video_capture.isOpened() and right_camera.video_capture.isOpened():

        cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

        while True:
            left_image, right_image = left_camera.read()[1], right_camera.read()[1]
                               
            # Use numpy to place images next to each other
            frames = np.hstack((left_image, right_image))
            if plot:
                cv2.imshow(window_title, frames)
                #limg = cv2.resize(left_image, (W, H))
                #lvid.write(limg.astype(np.uint8))
                #rimg = cv2.resize(right_image, (W, H))
                #rvid.write(rimg.astype(np.uint8))
            else:
                client.send(frames)
                # Stop the program on the ESC key
            if cv2.waitKey(30) == 27:
                break
        left_camera.stop()
        right_camera.stop()
        cv2.destroyAllWindows()
