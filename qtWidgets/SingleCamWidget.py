import os, sys
import numpy as np
import cv2
import time
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

dispH, dispW = 1216, 1936
def cv2_video_writer(w=1280, h=720):
    # camera init
    fps = 10 # int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    vid_writer = cv2.VideoWriter('output.mp4', fourcc, fps, (w, h))
    return vid_writer


class SingleCamWidget(QWidget):
    def __init__(self, server, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.vid_writer = cv2_video_writer(w=1280, h=720)
        self.server = server
        self.size = 256
        self.video_size = QSize(self.size*2, self.size*2)
        self.server_sokect = None
        self.image = None
        self.predict_time = None
        self.setup_ui()
        self.plot_fps(initial=True)
        self.start_sokect()
        
        #self.video = cv2.VideoCapture(0)
    def setup_ui(self):
        """Initialize widgets.
        """
        self.set1_video_bar_layout()
        self.set2_main_layout()
        
    def set1_video_bar_layout(self):
        # Predicted time bar
        self.predictor_layout = QHBoxLayout()
        self.predictor_title = QLabel('Predicted time')
        self.predictbar = QLabel('', self)
        self.predictbar.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.predictor_layout.addWidget(self.predictor_title)
        self.predictor_layout.addWidget(self.predictbar)
        
        # video widget
        self.video_widget = QLabel()
        self.video_widget.setFixedSize(self.video_size)
        
    def set2_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.video_widget)
        self.main_layout.addLayout(self.predictor_layout)
        self.setLayout(self.main_layout)
        
    def start_sokect(self):
        """Start Socket
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.recieve)
        self.timer.start(30)
        #self.timer.update()
        
    def recieve(self):
        """Read frame from camera and repaint QLabel widget.
        """
        #ret, self.frame = self.video.read()
        #self.image = self.openCV2Qimage(self.frame)
        time.sleep(5)
        conn, addr = self.server_sokect.accept()
        data = b""
        payload_size = self.server._struct_calcsize()
        print("payload_size: {}".format(payload_size))
        while True:
            start = time.time()
            while len(data) < payload_size:
                data += conn.recv(4096)

            data, msg_size = self.server._unpack_data(data, payload_size)
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = self.server._bts2img(frame_data)
            self.frame = cv2.resize(frame, (self.size, self.size))
            self.image = self.openCV2Qimage(self.frame)
            self.predict_time = np.round((time.time() - start), decimals=5)
            self.plot_fps()
      
    def openCV2Qimage(self, cvImage):
        height, width, channel = cvImage.shape
        bytesPerLine = channel * width
        cvImageRGB = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        image = QImage(cvImageRGB, width, height, bytesPerLine, QImage.Format_RGB888)
        return image
        
    def plot_fps(self, initial=None):
        if initial:
            self.server_sokect = self.server.accept_socket()
            self.predictbar.setText('now loading')
        if self.image is not None:
            self.video_widget.setPixmap(QPixmap.fromImage(self.image))
            im_rgb = cv2.resize(self.frame.copy(), (1280, 720))
            self.vid_writer.write(im_rgb.astype(np.uint8))
        if self.predict_time is not None:
            self.predictbar.setText(str(self.predict_time*1000)+"[ms]")
            
