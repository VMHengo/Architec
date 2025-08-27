import sys
import os
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QWidget
from PySide6.QtGui import QPixmap, QPainter, QImage, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt

project_dir = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QMainWindow):
    def __init__(self, ui_file_path):
        super().__init__()

        # Load the .ui file
        loader = QUiLoader()
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"Cannot open {ui_file_path}")

        self.ui = loader.load(ui_file)  # Load UI as a QWidget
        ui_file.close()

        if self.ui is None:
            raise RuntimeError("Failed to load UI")

        # Set window Icon
        self.setWindowIcon(QIcon(f"{project_dir}/assets/icon.ico"))

        # Set the loaded UI as central widget
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Architec 0.1")

        # Automatically assign all child widgets as attributes
        self._assign_widgets(self.ui)

        # Setup graphics view
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        # --- Connect menu action ---
        self.actionLoadImage = self.menuFile.addAction("Load Image")
        self.actionLoadImage.triggered.connect(self.load_image)

        self.actionCannyEdge = self.menuTools.addAction("Canny Edge")
        self.actionCannyEdge.triggered.connect(self.apply_canny_edge)

        # Track last used directory
        self.last_dir = ""

    def _assign_widgets(self, widget):
        """Recursively assign all child widgets as attributes."""
        for child in widget.findChildren(QWidget):
            name = child.objectName()
            if name:
                setattr(self, name, child)
                # Recursively assign children
                self._assign_widgets(child)


    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            self.last_dir if self.last_dir else project_dir,
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not file_path:
            raise RuntimeError("No file selected")

        self.last_dir = os.path.dirname(file_path)

        # --- Load image with OpenCV ---
        img = cv2.imread(file_path)
        if img is None:
            raise RuntimeError("Failed to load image")

        orig_height, orig_width = img.shape[:2]
        target_width = self.graphicsView.width()
        target_height = self.graphicsView.height()

        # --- Compute new size keeping aspect ratio ---
        scale_w = target_width / orig_width
        scale_h = target_height / orig_height
        scale = min(scale_w, scale_h)  # scale to fit inside view

        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)

        # --- Resize with high-quality interpolation ---
        resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

        # --- Convert to QPixmap ---
        qimg = QImage(
            resized.data,
            resized.shape[1],
            resized.shape[0],
            resized.strides[0],
            QImage.Format_BGR888
        )
        pixmap = QPixmap.fromImage(qimg)

        # --- Display in QGraphicsView ---
        self.scene.clear()
        pixmap_item = self.scene.addPixmap(pixmap)
        pixmap_item.setTransformationMode(Qt.SmoothTransformation)

        self.graphicsView.setRenderHint(QPainter.SmoothPixmapTransform)
        self.graphicsView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)


    def apply_canny_edge(self):
        # Check if there is a pixmap loaded
        if self.scene.items():
            # Get the current pixmap from the scene
            pixmap = self.scene.items()[0].pixmap()

            # Convert QPixmap to QImage
            qimg = pixmap.toImage().convertToFormat(QImage.Format.Format_BGR888)

            # Create NumPy array from memoryview
            width = qimg.width()
            height = qimg.height()
            img = qimg.bits()
            img = np.array(img).reshape(height, width, 3)

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Optional blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
            # Apply Canny
            edges = cv2.Canny(blurred, 50, 150)
            # Convert edges to BGR so QPixmap can display it
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

            # Convert back to QPixmap
            qimg_edges = QImage(edges_bgr.data, edges_bgr.shape[1], edges_bgr.shape[0],
                                edges_bgr.strides[0], QImage.Format_BGR888)
            pixmap_edges = QPixmap.fromImage(qimg_edges)

            # Display in scene
            self.scene.clear()
            edge_item = self.scene.addPixmap(pixmap_edges)
            edge_item.setTransformationMode(Qt.SmoothTransformation)
            self.graphicsView.setRenderHint(QPainter.SmoothPixmapTransform)
            self.graphicsView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        else:
            raise RuntimeError("No image loaded to process.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_file_path = os.path.join(project_dir, "form.ui")
    window = MainWindow(ui_file_path)
    window.showMaximized()
    sys.exit(app.exec())
