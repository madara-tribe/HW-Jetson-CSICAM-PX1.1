from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class LeftWidget(QWidget):
    def __init__(self, parent, click_event):
        super(LeftWidget, self).__init__(parent)
        
        self.layout = QVBoxLayout()
        self.button = QPushButton('Start', self) 
        self.click_event = click_event
        self.setUI()
            
    def setUI(self):
        self.button.clicked.connect(self.click_event)
        self.button.resize(100,32)
        self.layout.addWidget(self.button)
