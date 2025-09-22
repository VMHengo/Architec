# This Python file uses the following encoding: utf-8
import cv2
import os
import subprocess
import numpy as np
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QDialogButtonBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QImage, QIcon
from ui_canny_dialog import Ui_Dialog


TESTING = False
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if TESTING:
    UI_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "ui", "canny_dialog.ui"))
    PY_FILE = os.path.abspath(os.path.join(BASE_DIR, "ui_canny_dialog.py"))
    UIC_EXE = os.path.join(BASE_DIR, "..", ".qtcreator", "Python_3_10_10venv", "Scripts", "pyside6-uic.exe")

    # Automatically regenerate Python file from UI if needed
    if not os.path.exists(PY_FILE) or os.path.getmtime(UI_FILE) > os.path.getmtime(PY_FILE):
        subprocess.run([UIC_EXE, UI_FILE, "-o", PY_FILE], check=True)

class CannyDialog(QDialog, Ui_Dialog):

    sendImage = Signal(object)
    requestImage = Signal()

    def __init__(self, original_img, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Canny Edge Settings")

        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.imageData = original_img
        self.processed_img = None

        # button box
        apply_btn = self.buttonBox.button(QDialogButtonBox.Apply)
        cancel_btn = self.buttonBox.button(QDialogButtonBox.Cancel)
        reset_btn = self.buttonBox.button(QDialogButtonBox.Reset)

        # dont know why values in ui dont work
        self.slider_upperThresh.setMinimum(0)
        self.slider_upperThresh.setMaximum(300)
        self.slider_upperThresh.setValue(150)
        self.slider_upperThresh.setSingleStep(1)
        self.slider_upperThresh.setPageStep(10)

        # Connect signals
        apply_btn.clicked.connect(self.apply_canny_edge)
        cancel_btn.clicked.connect(self.reject)
        reset_btn.clicked.connect(self.on_reset)
        self.slider_upperThresh.valueChanged.connect(self.update_thresholds)
        self.slider_lowerThresh.valueChanged.connect(self.update_thresholds)

    def update_thresholds(self):
        t1 = self.slider_upperThresh.value()
        t2 = self.slider_lowerThresh.value()
        self.label_upper.setText(f"Threshold: {t1}")
        self.label_lower.setText(f"Threshold: {t2}")

        if self.checkBox_toggleLive.isChecked():
            self.apply_canny_edge()

    def apply_canny_edge(self):
        t1 = self.slider_lowerThresh.value()
        t2 = self.slider_upperThresh.value()

        # image processing for canny edge
        gray = cv2.cvtColor(self.imageData, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
        edges = cv2.Canny(blurred, t1, t2)
        self.processed_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        self.sendProcessedImage()

    def reject(self):
        self.accept()

    def on_reset(self):
        self.processed_img = None
        self.sendImage.emit(self.imageData)

    # --- Signal functions ---

    def receiveImage(self, img):
        self.imageData = img

    def sendProcessedImage(self):
        if self.processed_img.any():
            self.sendImage.emit(self.processed_img)
