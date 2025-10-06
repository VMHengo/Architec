# This Python file uses the following encoding: utf-8
import cv2
import os
import subprocess
import numpy as np
import scipy.spatial.distance as scipy_spatial_dist
from concurrent.futures import ThreadPoolExecutor
from sklearn.linear_model import RANSACRegressor, LinearRegression
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QDialogButtonBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QImage, QIcon
from ui_python.ui_vanishing_point_dialog import Ui_Dialog


TESTING = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if TESTING:
    UI_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "ui", "vanishing_point_dialog.ui"))
    PY_FILE = os.path.abspath(os.path.join(BASE_DIR, "ui_python", "ui_vanishing_point_dialog.py"))
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
        apply_btn.clicked.connect(self.find_vanishing_points)
        cancel_btn.clicked.connect(self.reject)
        reset_btn.clicked.connect(self.on_reset)
        save_btn.clicked.connect(self.save)

    def find_edges(self, method = "canny"):
        lines = None

        gray = cv2.cvtColor(self.imageData, cv2.COLOR_BGR2GRAY)
        preprocessed = cv2.GaussianBlur(gray, (5,5), 1.5)

        if method == "canny":
            edges = cv2.Canny(preprocessed, threshold1=50, threshold2=150)
            lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=120,
                                        minLineLength=50, maxLineGap=10)

        return lines

    # --- main vanishing point function ---
    def find_vanishing_points(self):

        #lsd = cv2.createLineSegmentDetector(0)
        #lines,_,_,_ = lsd.detect(gray)
        lines = self.find_edges(method="canny")

        segments = []
        for l in lines:
            x1, y1, x2, y2 = l[0]
            segments.append(((x1, y1), (x2, y2)))

        vps = self.vp_candidates_from_lines(segments, 2000)
        scores = self.score_vps(vps, segments)
        vps_pd, vps_idx = self.topk_orthogonal_vps(scores, vps, num_vps=3)
        print("Predicted Manhattan vanishing points:", vps_pd)

        self.draw_vps(lines, vps_pd)

    # --- vanishing point helper functions ---

    def draw_vps(self, lines, vps_pd):
        """Visualize lines and predicted VPs in your program."""

        self.processed_img = self.imageData.copy()

        H, W = self.imageData.shape[:2]
        cx, cy = W/2, H/2

        vp_img = []
        for vp in vps_pd:
            # Correct perspective projection
            x = (vp[0]/vp[2]) + cx
            y = (vp[1]/vp[2]) + cy
            vp_img.append((x, y))

        if lines is not None:
            for l in lines:
                x1, y1, x2, y2 = map(int, l[0])
                cv2.line(self.processed_img, (x1, y1), (x2, y2), (0, 0, 255), 1)
        for (x, y) in vp_img:
            cv2.circle(self.processed_img, center=(int(x), int(y)), radius=10, color=(0, 255, 0), thickness=10)

        self.sendProcessedImage()

    def line_to_homogeneous(self, p1, p2):
        """Convert 2D line segment endpoints into homogeneous line representation ax+by+c=0."""
        x1, y1 = p1
        x2, y2 = p2
        line = np.cross([x1, y1, 1.0], [x2, y2, 1.0])  # homogeneous line
        return line / np.linalg.norm(line[:2])  # normalize (a,b)

    def intersect_lines(self, l1, l2):
        """Intersect two homogeneous lines → returns homogeneous point."""
        pt = np.cross(l1, l2)
        if abs(pt[2]) < 1e-9:  # parallel lines
            return None
        return pt / pt[2]  # normalize to (x,y,1)

    def vp_candidates_from_lines(self, lines, max_samples=2000):
        """Generate candidate vanishing points by intersecting random line pairs."""
        hom_lines = [self.line_to_homogeneous(p1, p2) for (p1,p2) in lines]
        vps = []
        H, W = self.imageData.shape[:2]  # assume image scale for normalization
        for _ in range(max_samples):
            i, j = np.random.choice(len(hom_lines), 2, replace=False)
            pt = self.intersect_lines(hom_lines[i], hom_lines[j])
            if pt is None:
                continue
            # Convert to direction on Gaussian sphere
            # Center image: principal point (cx,cy) assumed at (W/2,H/2)
            cx, cy = W/2, H/2
            x, y = pt[0]-cx, pt[1]-cy
            z = W  # focal length proxy
            vec = np.array([x,y,z])
            vec = vec / np.linalg.norm(vec)
            vps.append(vec)
        return np.array(vps)

    def score_vps(self, vps, lines, thresh=2.0):
        """Score candidate vanishing points by how well they align with lines."""
        scores = []
        hom_lines = [self.line_to_homogeneous(p1, p2) for (p1,p2) in lines]
        for vp in vps:
            d = vp[:2] / (vp[2] + 1e-9)
            angle_vp = np.arctan2(d[1], d[0])
            line_angles = [np.arctan2(l[0], -l[1]) for l in hom_lines]
            diffs = np.abs(np.unwrap(line_angles) - angle_vp)
            aligned = np.sum(diffs < np.deg2rad(thresh))
            scores.append(aligned)
        return np.array(scores)

    def topk_orthogonal_vps(self, scores, xyz, num_vps=3):
        """Select up to num_vps vanishing points with orthogonality constraint."""
        index = np.argsort(-scores)
        vps_idx = [index[0]]
        for i in index[1:]:
            if len(vps_idx) == num_vps:
                break
            dist_cos = scipy_spatial_dist.cdist(xyz[vps_idx], xyz[i][None, :], 'cosine')
            dist_cos = np.abs(-1.0*dist_cos+1.0)
            dist_cos_arc = np.min(np.arccos(dist_cos))
            if dist_cos_arc >= np.pi/num_vps:
                vps_idx.append(i)
        vps_pd = xyz[vps_idx]
        return vps_pd, vps_idx

    # --- ui interface functions ---

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
