import sys
import cv2

# GStreamer pipeline
def gstreamer_pipeline(hyp):
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
            hyp['capture_width'],
            hyp['capture_height'],
            hyp['framerate'],
            hyp['flip_method'],
            hyp['display_width'],
            hyp['display_height'],
        )
    )

def run_csicam(hyp, client=None, plot=None):
    cap = cv2.VideoCapture(gstreamer_pipeline(hyp), cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print('Can not open camera.')
        sys.exit()

    while True:
        ret, frame = cap.read()
        if plot:
            cv2.imshow('Viewer', frame)
        else:
            client.send(frame)
        if cv2.waitKey(30) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
