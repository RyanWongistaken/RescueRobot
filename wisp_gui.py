import sys, random, time, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from HUD import *
from sensor import *
import cv2

class HUD(QWidget):
    def __init__(self):
        super().__init__() # Run QWidget init
        self.vid = Video() # Create video object
        self.setWindowTitle("WISP")
        self.setGeometry(0, 0, 720, 480)
        self.initHUD()
        self.show()

    # Setup Window
    def initHUD(self):
        self.layout = QGridLayout()
        self.vid.start_camera()
        # Add Widget to Layout
        self.layout.addWidget(self.vid.picture,0,0)
        self.layout.addWidget(self.vid.gui, 0, 0)
        # Display Window
        self.setLayout(self.layout)


class Video(QWidget):
    def __init__(self):
        super().__init__()  # Run QWidget init
        self.timer = QTimer(self)
        self.HudTimer = QTimer(self)
        self.fps = 30 # Set fps update rate
        self.picture = QLabel()
        self.gui = QLabel()
        self.test = 0
        


    # Start Camera
    @pyqtSlot()
    def start_camera(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


        if not self.cam.isOpened():
            popUp = QMessageBox()
            popUp.setWindowTitle("WISP")
            popUp.setText("Failed to Open Camera")
            popUp.exec_()
            return
        self.timer.timeout.connect(self.update)
        self.HudTimer.timeout.connect(self.refresh)
        self.HudTimer.start(1000.)
        self.timer.start(1000. /self.fps) # start once every 41msec

    # Draw the new frame to replace the old one
    @pyqtSlot()
    def update(self):
        ret, frame = self.cam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Webcam is in BGR needs to be converted
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.picture.setPixmap(pix)

        
    # Draws hud overtop frame    
    @pyqtSlot()
    def refresh(self):
        sensoPlug = GetData()
        print(sensoPlug[2])
        Overlay(sensoPlug[2], sensoPlug[1], sensoPlug[3], sensoPlug[0])
        #self.test += 1
        #Overlay(45+self.test, 12+self.test, -50+self.test, self.test)
        self.gui.setPixmap(QPixmap('hud.png'))
        



def main():
    app = QApplication([])
    gui = HUD()
    app.exec_()
    print("pain!")
main()