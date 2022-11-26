import sys
import cv2

# GStreamer pipeline
def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def run_csicam(opt, client):
    cap = cv2.VideoCapture(gstreamer_pipeline(display_width=640, display_height=360), cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print('Can not open camera.')
        sys.exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        #cv2.imshow('Viewer', frame)
        client.send(frame)
        if cv2.waitKey(30) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
