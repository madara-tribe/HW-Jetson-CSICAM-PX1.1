import os
import cv2
import time
import numpy as np
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QLabel

dispH, dispW = 720, 1280
def cv2_video_writer(w=dispW, h=dispH):
    # camera init
    fps = 10 # int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    vid_writer = cv2.VideoWriter('output.mp4', fourcc, fps, (w, h))
    return vid_writer
    

class Thread(QThread):
    updateFrame = Signal(QImage)
    def __init__(self, parent=None, vid_size=None, server=None, opt=None):
        QThread.__init__(self, parent)
        self.opt = opt
        self.cap = cv2.VideoCapture(0)
        self.pred_time = 0
        self.vid_side = vid_size
        self.server = server
        self.vid_writer = cv2_video_writer(w=1280, h=720)
        self.vid = True
        self.server_sokect = self.server.accept_socket()
        
    def openCV2Qimage(self, cvImage):
        if self.opt.dual:
            cvImage = cv2.resize(cvImage, (self.vid_side*2, self.vid_side))
        else:
            cvImage = cv2.resize(cvImage, (self.vid_side, self.vid_side))
        height, width, channel = cvImage.shape
        bytesPerLine = channel * width
        cvImageRGB = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        image = QImage(cvImageRGB, width, height, bytesPerLine, QImage.Format_RGB888)
        return image
    
    def run(self):
        """Read frame from camera and repaint QLabel widget.
        """
        conn, addr = self.server_sokect.accept()
        data = b""
        payload_size = self.server._struct_calcsize()
        print("payload_size: {}".format(payload_size))
        while True:
            start = time.time()
            ##### tcp recieve #####
            while len(data) < payload_size:
                data += conn.recv(4096)

            data, msg_size = self.server._unpack_data(data, payload_size)
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = self.server._bts2img(frame_data)
            ########################
            
            # Creating and scaling QImage
            img = self.openCV2Qimage(frame)
            scaled_img = img.scaled(self.vid_side, self.vid_side, Qt.KeepAspectRatio)
            self.pred_time = np.round((time.time() - start), decimals=5)
            
            # Emit signal
            self.updateFrame.emit(scaled_img)
            if self.vid:
                im_rgb = cv2.resize(frame.copy(), (dispW, dispH))
                self.vid_writer.write(im_rgb.astype(np.uint8))
        sys.exit(-1)

    def justPlot(self):
        """ Replace by rename run() function if you want to just plot image"""
        while True:
            ret, frame = self.cap.read()
            stime = time.time()
            
            # Creating and scaling QImage
            img = self.openCV2Qimage(frame)
            scaled_img = img.scaled(self.vid_side, self.vid_side, Qt.KeepAspectRatio)
            self.pred_time = np.round((time.time() - stime), decimals=5)
            
            # Emit signal
            self.updateFrame.emit(scaled_img)
            if self.vid:
                im_rgb = cv2.resize(frame.copy(), (dispW, dispH))
                self.vid_writer.write(im_rgb.astype(np.uint8))
        sys.exit(-1)
        
        
    
