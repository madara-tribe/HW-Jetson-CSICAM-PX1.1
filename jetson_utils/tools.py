import cv2

W=1280
H=720
def cv2_video_writer(w, h, filename='output.mov'):
    # camera init
    fps = 10 # int(cap.get(cv2.CAP_PR
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    vid_writer = cv2.VideoWriter(filename, fourcc, fps, (w, h))
    return vid_writer
