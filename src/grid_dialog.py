# This Python file uses the following encoding: utf-8
import cv2
import os
import subprocess
import numpy as np
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QDialogButtonBox, QStyleFactory, QGraphicsScene
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QImage, QIcon, QColor
from ui_python.ui_grid_dialog import Ui_Dialog


TESTING = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if TESTING:
    UI_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "ui", "grid_dialog.ui"))
    PY_FILE = os.path.abspath(os.path.join(BASE_DIR, "ui_python", "ui_grid_dialog.py"))
    UIC_EXE = os.path.join(BASE_DIR, "..", ".qtcreator", "Python_3_10_10venv", "Scripts", "pyside6-uic.exe")

    # Automatically regenerate Python file from UI if needed
    if not os.path.exists(PY_FILE) or os.path.getmtime(UI_FILE) > os.path.getmtime(PY_FILE):
        subprocess.run([UIC_EXE, UI_FILE, "-o", PY_FILE], check=True)

class GridDialog(QDialog, Ui_Dialog):

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

        # slider setup
        self.setup_sliders(self.slider_resolution, 2, 30, 10, 1, 10)
        self.setup_sliders(self.slider_lineThickness, 1, 30, 5, 1, 10)
        self.setup_colorSelect()

        # Connect signals
        apply_btn.clicked.connect(self.draw_grid)
        cancel_btn.clicked.connect(self.reject)
        reset_btn.clicked.connect(self.on_reset)

        self.slider_resolution.valueChanged.connect(self.update_thresholds)
        self.slider_lineThickness.valueChanged.connect(self.update_thresholds)

        self.selectedColor = {
            "red" : 0,
            "green" : 0,
            "blue" : 0
        }
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor(self.selectedColor["red"], self.selectedColor["green"], self.selectedColor["blue"]))
        self.graphicsView_colorShow.setScene(self.scene)

    def setup_colorSelect(self):

        for color in ["red", "green", "blue"]:
            scrollbar = getattr(self, f"scrollBar_{color}")
            scrollbar.valueChanged.connect(lambda _, c = color: self.update_spinBox(c))

            spinBox = getattr(self, f"spinBox_rgb_{color}")
            spinBox.valueChanged.connect(lambda _, c = color: self.update_scrollBar(c))

        to_style_change = [
            self.spinBox_rgb_red,
            self.spinBox_rgb_green,
            self.spinBox_rgb_blue,
            self.scrollBar_red,
            self.scrollBar_green,
            self.scrollBar_blue,
        ]
        self.setStyle(to_style_change, "Fusion")
        self.spinBox_rgb_red.setStyle(QStyleFactory.create("Fusion"))

    def setup_sliders(self, slider, min, max, val, singleStep, pageStep):
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setValue(val)
        slider.setSingleStep(singleStep)
        slider.setPageStep(pageStep)

    def update_thresholds(self):
        t1 = self.slider_resolution.value()
        t2 = self.slider_lineThickness.value()
        self.label_resolution.setText(f"Resolution: {t1}")
        self.label_lineThickness.setText(f"Line Thickness: {t2}")

        if self.checkBox_toggleLive.isChecked():
            self.draw_grid()

    def update_spinBox(self, color):
        value = getattr(self, f"scrollBar_{color}").value()
        spinBox = getattr(self, f"spinBox_rgb_{color}")
        spinBox.setValue(value)
        self.selectedColor[color] = value
        self.update_colorShow()

    def update_scrollBar(self, color):
        value = getattr(self, f"spinBox_rgb_{color}").value()
        scrollBar = getattr(self, f"scrollBar_{color}")
        scrollBar.setValue(value)
        self.selectedColor[color] = value
        self.update_colorShow()

    def update_colorShow(self):
        self.scene.setBackgroundBrush(QColor(self.selectedColor["red"], self.selectedColor["green"], self.selectedColor["blue"]))

        if self.checkBox_toggleLive.isChecked():
            self.draw_grid()

    # --- Button functions ---

    def draw_grid(self):
        img = self.processed_img = self.imageData.copy()
        height = img.shape[0]
        width = img.shape[1]
        lineThickness = self.slider_lineThickness.value()
        resolution = self.slider_resolution.value()

        rect_size = max(height, width) / resolution

        for i in range(1, resolution):
            color = (self.selectedColor["blue"], self.selectedColor["green"], self.selectedColor["red"])
            dim = round(i*rect_size)
            cv2.line(img, (dim,0), (dim, height), color, lineThickness)
            cv2.line(img, (0, dim), (width, dim), color, lineThickness)

        self.processed_img = img
        self.sendProcessedImage()

    def reject(self):
        self.accept()

    def on_reset(self):
        self.processed_img = None
        self.sendImage.emit(self.imageData.copy())

    # --- Signal functions ---

    def receiveImage(self, img):
        self.imageData = img.copy()
        self.processed_img = self.imageData
        self.sendProcessedImage()

    def sendProcessedImage(self):
        if self.processed_img.any():
            self.sendImage.emit(self.processed_img.copy())

    # --- helper functions

    def setStyle(self, tobeChanged, style):
        for element in tobeChanged:
            element.setStyle(QStyleFactory.create(style))
