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
    def __init__(self, server_sokect, parent=None):
        super().__init__(parent)
        
        self.parent = parent
        self.vid_writer = cv2_video_writer(w=1280, h=720)
        self.server_sokect = server_sokect
        self.vid_capture = cv2.VideoCapture(0)
        self.size = 256
        self.video_size = QSize(self.size*2, self.size*2)
        self.cur_fps = 0
        self.setup_ui()
        self.plot_fps(initial=True)
        
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

        # start button
        self.button = QPushButton("Start Recieve")
        self.button.setFixedSize(100, 40)
        self.button.setStyleSheet('background-color: white')
        self.button.clicked.connect(self.start_sokect)
        
        # video widget
        self.video_widget = QLabel()
        self.video_widget.setFixedSize(self.video_size)
        
    def set2_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.video_widget)
        self.main_layout.addWidget(self.button)
        self.main_layout.addLayout(self.predictor_layout)
        self.setLayout(self.main_layout)
        
    def start_sokect(self):
        """Start Socket
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.recieve)
        self.timer.start(30)
        
    def recieve(self, vid=True):
        """Read frame from camera and repaint QLabel widget.
        """
        #_, frame = self.vid_capture.read()
        try:
            start = time.time()
            frame = self.server_sokect.recieve()
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_ = cv2.resize(frame, (self.size, self.size))
            #pred_frame = np.hstack([pred_frame, pred_frame])
            image = QImage(frame_, frame_.shape[1], frame_.shape[0],
                                        frame_.strides[0], QImage.Format_RGB888)
            self.video_widget.setPixmap(QPixmap.fromImage(image))
            self.predict_time = np.round((time.time() - start), decimals=5)
            self.plot_fps()
            if vid:
                im_rgb = cv2.resize(frame.copy(), (1280, 720))
                self.vid_writer.write(im_rgb.astype(np.uint8))
        except KeyboardInterrupt:
             sys.exit()
        
    def plot_fps(self, initial=None):
        if initial:
            self.server_sokect.accept()
            self.predictbar.setText("now loading")
        else:
            self.predictbar.setText(str(self.predict_time*1000)+"[ms]")
            
