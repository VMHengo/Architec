import sys
import os
import cv2
import subprocess
import numpy as np
from appdirs import user_data_dir
from PySide6.QtWidgets import QDialog, QApplication, QMainWindow, QFileDialog, QGraphicsScene, QWidget
from PySide6.QtGui import QPixmap, QPainter, QImage, QIcon, QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QSettings

from ui_python.ui_form import Ui_MainWindow
from canny_dialog import CannyDialog
from grid_dialog import GridDialog
from vanishing_point_dialog import VanishingPointDialog
from recent_files import add_recent_file, load_recent_files


APP_NAME = "Architec"
APP_AUTHOR = "HoangNguyen"

TESTING = True
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

if TESTING:

    UI_FILE = os.path.join(PROJECT_DIR, "ui", "form.ui")
    PY_FILE = os.path.join(PROJECT_DIR, "src", "ui_python", "ui_form.py")
    UIC_EXE = os.path.join(PROJECT_DIR, ".qtcreator", "Python_3_10_10venv", "Scripts", "pyside6-uic.exe")

    # Automatically regenerate Python file from UI if needed
    if not os.path.exists(PY_FILE) or os.path.getmtime(UI_FILE) > os.path.getmtime(PY_FILE):
        subprocess.run([UIC_EXE, UI_FILE, "-o", PY_FILE], check=True)


# ---- MAIN CLASS ----

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cv_image = None # type: np array

        self._ui_init()
        self._dialog_init()
        self._menuBar_init()


        self.last_dir = None
        self.current_file_path = None


    # --- "private" functions ---

    def _ui_init(self):
        icon_filePath = os.path.join(PROJECT_DIR, "assets", "icon.ico")
        self.setWindowIcon(QIcon(icon_filePath))
        self.setWindowTitle("Architec 0.1")

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

    def _dialog_init(self):
        self.canny_dialog = CannyDialog(self.cv_image, self)
        self.vp_dialog = VanishingPointDialog(self.cv_image, self)
        self.grid_dialog = GridDialog(self.cv_image, self)
        self.dialogs = [self.canny_dialog, self.vp_dialog, self.grid_dialog]

    def _menuBar_init(self):
        # File tab
        actionLoadImage = self.menuFile.addAction("Open Image")
        actionLoadImage.triggered.connect(self.open_image)

        self.menuRecentFiles = self.menuFile.addMenu("Open recent files")
        self.menuRecentFiles.addAction("(No recent files)").setEnabled(False)

        actionSaveImage = self.menuFile.addAction("Save Image")
        actionSaveImage.triggered.connect(self.save_image)

        actionSaveImageAs = self.menuFile.addAction("Save Image as...")
        actionSaveImageAs.triggered.connect(self.save_image_as)

        # Tools tab
        actionCannyEdge = self.menuTools.addAction("Canny Edge")
        actionCannyEdge.triggered.connect(self.open_canny_dialog)

        actionVanishingPoint = self.menuTools.addAction("Find Vanishing Point")
        actionVanishingPoint.triggered.connect(self.open_vanishing_point_dialog)

        actionDrawGrid = self.menuTools.addAction("Draw grid")
        actionDrawGrid.triggered.connect(self.open_grid_dialog)

        # updates
        self.update_recent_files_menu()


    # --- "public" functions ---

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            self.last_dir if self.last_dir else PROJECT_DIR,
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            raise RuntimeError("No file selected")

        self.update_file_history(file_path)


    # Menubar [ File ] functions

    def load_image(self, file_path):
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

        for dialog in self.dialogs:
            dialog.imageData = self.cv_image.copy()

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

    def save_image(self):
        if self.current_file_path:
            cv2.imwrite(self.current_file_path, self.cv_image)
        else:
            self.save_image_as()

    def save_image_as(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None,
                                                   "Save Image As",
                                                   "",
                                                   "JPEG Files (*.jpg);;PNG Files (*.png);;All Files (*)",
                                                   options=options)
        if file_path:
            self.current_file_path = file_path
            cv2.imwrite(file_path, self.cv_image)


    # Menubar [ Tools ] functions

    def open_canny_dialog(self):
        self.dialogs[0] = CannyDialog(self.cv_image, self)
        self.canny_dialog = self.dialogs[0]
        self.canny_dialog.sendImage.connect(self.handle_processed_image)
        self.canny_dialog.requestImage.connect(self.handle_request_image)
        self.canny_dialog.show()

    def open_vanishing_point_dialog(self):
        self.dialogs[1] = VanishingPointDialog(self.cv_image, self)
        self.vp_dialog = self.dialogs[1]
        self.vp_dialog.sendImage.connect(self.handle_processed_image)
        self.vp_dialog.requestImage.connect(self.handle_request_image)
        self.vp_dialog.show()

    def open_grid_dialog(self):
        self.dialogs[2] = GridDialog(self.cv_image, self)
        self.grid_dialog = self.dialogs[2]
        self.grid_dialog.sendImage.connect(self.handle_processed_image)
        self.grid_dialog.requestImage.connect(self.handle_request_image)
        self.grid_dialog.show()


    # Display functions

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


    # MOSI communication functions

    def handle_request_image(self):
        sender = self.sender()
        if sender:
            sender.receiveImage(self.cv_image.copy())

    def handle_processed_image(self, img):
        sender = self.sender()
        if sender:
            self.cv_image = img
            self.display_image_data(self.cv_image)


    # update functions

    def update_recent_files_menu(self):
        self.menuRecentFiles.clear()
        recent_files = load_recent_files()

        if not recent_files:
                self.menuRecentFiles.addAction("(No recent files)").setEnabled(False)
                return

        for entry in load_recent_files():
            path = entry["path"]
            if not os.path.exists(path):
                continue

            action = QAction(os.path.basename(path), self)
            action.setToolTip(path)
            action.triggered.connect(lambda checked=False, p=path: self.load_image(p))
            self.menuRecentFiles.addAction(action)

    def update_file_history(self, file_path):
        self.load_image(file_path)
        self.current_file_path = file_path
        self.last_dir = os.path.dirname(file_path)
        add_recent_file(file_path)
        self.update_recent_files_menu()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
