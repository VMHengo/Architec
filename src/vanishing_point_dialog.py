# This Python file uses the following encoding: utf-8
import cv2
import os
import subprocess
import numpy as np
from sklearn.linear_model import RANSACRegressor, LinearRegression
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QDialogButtonBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QImage, QIcon
from ui_vanishing_point_dialog import Ui_Dialog


TESTING = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if TESTING:
    UI_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "ui", "vanishing_point_dialog.ui"))
    PY_FILE = os.path.abspath(os.path.join(BASE_DIR, "ui_vanishing_point_dialog.py"))
    UIC_EXE = os.path.join(BASE_DIR, "..", ".qtcreator", "Python_3_10_10venv", "Scripts", "pyside6-uic.exe")

    # Automatically regenerate Python file from UI if needed
    if not os.path.exists(PY_FILE) or os.path.getmtime(UI_FILE) > os.path.getmtime(PY_FILE):
        subprocess.run([UIC_EXE, UI_FILE, "-o", PY_FILE], check=True)

class VanishingPointDialog(QDialog, Ui_Dialog):

    sendImage = Signal(object)
    requestImage = Signal()

    def __init__(self, original_img, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Find Vanishing Point")

        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.imageData = original_img
        self.processed_img = None

        # button box
        apply_btn = self.buttonBox.button(QDialogButtonBox.Apply)
        cancel_btn = self.buttonBox.button(QDialogButtonBox.Cancel)
        reset_btn = self.buttonBox.button(QDialogButtonBox.Reset)
        save_btn = self.buttonBox.button(QDialogButtonBox.Save)

        # Connect signals
        apply_btn.clicked.connect(self.find_vanishing_point)
        cancel_btn.clicked.connect(self.reject)
        reset_btn.clicked.connect(self.on_reset)
        save_btn.clicked.connect(self.save)

    def find_vanishing_point(self):
        gray = cv2.cvtColor(self.imageData, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
        edges = cv2.Canny(blurred, 50, 150)

        points = np.column_stack(np.where(edges > 0))

        X = points[:, 1].reshape(-1, 1)
        y = points[:, 0]

        lines = []
        for _ in range(5):
            if len(X) < 20:
                break
            ransac = RANSACRegressor(LinearRegression(), residual_threshold=2, max_trials=1000)
            ransac.fit(X, y)

            inlier_mask = ransac.inlier_mask_
            m = ransac.estimator_.coef_[0]   # slope
            b = ransac.estimator_.intercept_ # intercept

            # Compute two endpoints within image bounds
            x1, x2 = 0, gray.shape[1]
            y1 = int(m * x1 + b)
            y2 = int(m * x2 + b)

            lines.append((x1, y1, x2, y2))

            # remove inliers for next iteration
            X = X[~inlier_mask]
            y = y[~inlier_mask]

        def line_from_points(x1, y1, x2, y2):
            # returns line in ax + by + c = 0 form
            a = y1 - y2
            b = x2 - x1
            c = x1*y2 - x2*y1
            return a, b, c

        A = []
        for (x1, y1, x2, y2) in lines:
            a, b, c = line_from_points(x1, y1, x2, y2)
            A.append([a, b, c])
            cv2.line(self.imageData, (x1,y1), (x2,y2), (0,255,0), 2)

        A = np.array(A)

        # solve least squares intersection
        _, _, Vt = np.linalg.svd(A)
        vp = Vt[-1]
        vp = vp / vp[-1]   # homogeneous coords ➝ (x,y)
        vx, vy = int(vp[0]), int(vp[1])

        cv2.circle(self.imageData, (vx,vy), 10, (0,0,255), -1)
        self.processed_img = self.imageData
        self.sendProcessedImage()

    def reject(self):
        self.accept()

    def save(self):
        # TO BE IMPLEMENTED
        return

    def on_reset(self):
        self.processed_img = None
        self.sendImage.emit(self.imageData)

    # --- Signal functions ---

    def receiveImage(self, img):
        self.imageData = img

    def sendProcessedImage(self):
        if self.processed_img.any():
            self.sendImage.emit(self.processed_img)
