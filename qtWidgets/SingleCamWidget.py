import os, sys
import numpy as np
import cv2
import time
from PySide6.QtCore import Slot, QSize
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget)

from qtWidgets.VideoTread import Thread

class SingleCamWidget(QWidget):
    def __init__(self, server, opt, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.server = server
        self.opt = opt
        self.vid_size = 300
        self.setup_ui()
        self.set_thread(vid_size = self.vid_size, server=self.server, opt=self.opt)
        self.predictbar.setText('Now Loading')
        
    def set_thread(self, vid_size, server, opt):
        self.th = Thread(self, vid_size=vid_size, server=server, opt=opt)
        self.th.updateFrame.connect(self.setImage)
        self.th.updateFrame.connect(self.plot_fps)
        
    def setup_ui(self):
        """Initialize widgets.
        """
        self.set1_widget_layout()
        self.set2_main_layout()
        
    def set1_widget_layout(self):
        # Predicted time bar
        self.predictor_layout = QHBoxLayout()
        self.predictor_title = QLabel('Predicted time')
        self.predictbar = QLabel('', self)
        self.predictbar.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.predictbar.setFixedSize(QSize(200, 40))
        self.predictor_layout.addWidget(self.predictor_title)
        self.predictor_layout.addWidget(self.predictbar)
        
        # button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start)
        
        # video widget
        self.video_display = QLabel()
        self.video_display.setFixedSize(QSize(self.vid_size*2, self.vid_size*2))
        
    def set2_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.video_display)
        self.main_layout.addWidget(self.start_button)
        self.main_layout.addLayout(self.predictor_layout)
        self.setLayout(self.main_layout)
        
    def plot_fps(self, event):
        self.predictbar.setText(str(self.th.pred_time*1000)+"[ms]")
      
    @Slot()
    def start(self):
        print("Starting...")
        self.th.start()
        
    @Slot(QImage)
    def setImage(self, image):
        self.video_display.setPixmap(QPixmap.fromImage(image))
   
