import sys
import os
import cv2
import subprocess
import numpy as np
from PySide6.QtWidgets import QDialog, QApplication, QMainWindow, QFileDialog, QGraphicsScene, QWidget
from PySide6.QtGui import QPixmap, QPainter, QImage, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt

from ui_form import Ui_MainWindow
from canny_dialog import CannyDialog
from vanishing_point_dialog import VanishingPointDialog

TESTING = False
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

if TESTING:

    UI_FILE = os.path.join(PROJECT_DIR, "ui", "form.ui")
    PY_FILE = os.path.join(PROJECT_DIR, "src", "ui_form.py")
    UIC_EXE = os.path.join(PROJECT_DIR, ".qtcreator", "Python_3_10_10venv", "Scripts", "pyside6-uic.exe")

    # Automatically regenerate Python file from UI if needed
    if not os.path.exists(PY_FILE) or os.path.getmtime(UI_FILE) > os.path.getmtime(PY_FILE):
        subprocess.run([UIC_EXE, UI_FILE, "-o", PY_FILE], check=True)

# ---- MAIN CLASS ----
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cv_image = None

        icon_filePath = os.path.join(PROJECT_DIR, "assets", "icon.ico")
        self.setWindowIcon(QIcon(icon_filePath))
        self.setWindowTitle("Architec 0.1")

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.actionLoadImage = self.menuFile.addAction("Load Image")
        self.actionCannyEdge = self.menuTools.addAction("Canny Edge")
        self.actionVanishingPoint = self.menuTools.addAction("Find Vanishing Point")

        self.actionLoadImage.triggered.connect(self.load_image)
        self.actionCannyEdge.triggered.connect(self.open_canny_dialog)
        self.actionVanishingPoint.triggered.connect(self.open_vanishing_point_dialog)

        self.last_dir = ""

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            self.last_dir if self.last_dir else PROJECT_DIR,
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not file_path:
            raise RuntimeError("No file selected")

        self.last_dir = os.path.dirname(file_path)

        # Load image with OpenCV
        img = cv2.imread(file_path)
        if img is None:
            raise RuntimeError("Failed to load image")

        orig_height, orig_width = img.shape[:2]
        target_width = self.graphicsView.width()
        target_height = self.graphicsView.height()

        # Compute new size keeping aspect ratio
        scale_w = target_width / orig_width
        scale_h = target_height / orig_height
        scale = min(scale_w, scale_h)

        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)

        resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        self.cv_image = resized.copy()

        # Convert to QPixmap
        qimg = QImage(
            resized.data,
            resized.shape[1],
            resized.shape[0],
            resized.strides[0],
            QImage.Format_BGR888
        )
        pixmap = QPixmap.fromImage(qimg)

        self.display_pixmap(pixmap)

    def display_pixmap(self, pixmap):
        self.scene.clear()
        pixmap_item = self.scene.addPixmap(pixmap)
        pixmap_item.setTransformationMode(Qt.SmoothTransformation)
        self.graphicsView.setRenderHint(QPainter.SmoothPixmapTransform)
        self.graphicsView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def display_image_data(self, img):
        self.cv = img
        qimage = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(qimage)
        self.display_pixmap(pixmap)

    def open_canny_dialog(self):
        dialog = CannyDialog(self.cv_image, self)
        dialog.sendImage.connect(self.handle_processed_image)
        dialog.requestImage.connect(self.handle_request_image)
        dialog.show()

    def open_vanishing_point_dialog(self):
        dialog = VanishingPointDialog(self.cv_image, self)
        dialog.sendImage.connect(self.handle_processed_image)
        dialog.requestImage.connect(self.handle_request_image)
        dialog.show()
        self.open_canny_dialog()

    def handle_request_image(self):
        sender = self.sender()
        if sender:
            sender.receiveImage(self.cv_image)

    def handle_processed_image(self, img):
        sender = self.sender()
        if sender:
            self.cv_image = img
            self.display_image_data(self.cv_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
