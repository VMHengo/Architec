# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grid_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGraphicsView, QLabel, QScrollBar,
    QSizePolicy, QSlider, QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(446, 342)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(20, 300, 411, 32))
        self.buttonBox.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Reset)
        self.buttonBox.setCenterButtons(False)
        self.slider_resolution = QSlider(Dialog)
        self.slider_resolution.setObjectName(u"slider_resolution")
        self.slider_resolution.setGeometry(QRect(20, 13, 160, 16))
        self.slider_resolution.setOrientation(Qt.Orientation.Horizontal)
        self.slider_lineThickness = QSlider(Dialog)
        self.slider_lineThickness.setObjectName(u"slider_lineThickness")
        self.slider_lineThickness.setGeometry(QRect(20, 40, 160, 16))
        self.slider_lineThickness.setOrientation(Qt.Orientation.Horizontal)
        self.checkBox_toggleLive = QCheckBox(Dialog)
        self.checkBox_toggleLive.setObjectName(u"checkBox_toggleLive")
        self.checkBox_toggleLive.setGeometry(QRect(20, 60, 151, 18))
        self.label_resolution = QLabel(Dialog)
        self.label_resolution.setObjectName(u"label_resolution")
        self.label_resolution.setGeometry(QRect(190, 13, 171, 16))
        self.label_lineThickness = QLabel(Dialog)
        self.label_lineThickness.setObjectName(u"label_lineThickness")
        self.label_lineThickness.setGeometry(QRect(190, 40, 181, 16))
        self.scrollBar_red = QScrollBar(Dialog)
        self.scrollBar_red.setObjectName(u"scrollBar_red")
        self.scrollBar_red.setGeometry(QRect(20, 133, 211, 16))
        self.scrollBar_red.setStyleSheet(u"QScrollBar {\n"
"   background: rgb(255, 105, 97); /* \u2190 overall background area */\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: #666;   /* draggable handle */\n"
"    min-width: 15px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"	width: 0px;\n"
"	height: 0px;\n"
"	subcontrol-origin: margin;\n"
"}")
        self.scrollBar_red.setMaximum(255)
        self.scrollBar_red.setPageStep(10)
        self.scrollBar_red.setOrientation(Qt.Orientation.Horizontal)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 113, 101, 16))
        self.graphicsView_colorShow = QGraphicsView(Dialog)
        self.graphicsView_colorShow.setObjectName(u"graphicsView_colorShow")
        self.graphicsView_colorShow.setGeometry(QRect(330, 125, 91, 81))
        self.scrollBar_green = QScrollBar(Dialog)
        self.scrollBar_green.setObjectName(u"scrollBar_green")
        self.scrollBar_green.setGeometry(QRect(20, 158, 211, 16))
        self.scrollBar_green.setStyleSheet(u"QScrollBar {\n"
"    background: rgb(93, 186, 19); /* \u2190 overall background area */\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: #666;   /* draggable handle */\n"
"    min-width: 15px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"	width: 0px;\n"
"	height: 0px;\n"
"	subcontrol-origin: margin;\n"
"}")
        self.scrollBar_green.setMaximum(255)
        self.scrollBar_green.setOrientation(Qt.Orientation.Horizontal)
        self.scrollBar_blue = QScrollBar(Dialog)
        self.scrollBar_blue.setObjectName(u"scrollBar_blue")
        self.scrollBar_blue.setGeometry(QRect(20, 183, 211, 16))
        self.scrollBar_blue.setStyleSheet(u"QScrollBar {\n"
"    background: rgb(0, 186, 255); /* \u2190 overall background area */\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: #666;   /* draggable handle */\n"
"    min-width: 15px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"	width: 0px;\n"
"	height: 0px;\n"
"	subcontrol-origin: margin;\n"
"}")
        self.scrollBar_blue.setMaximum(255)
        self.scrollBar_blue.setOrientation(Qt.Orientation.Horizontal)
        self.label_rgb_red = QLabel(Dialog)
        self.label_rgb_red.setObjectName(u"label_rgb_red")
        self.label_rgb_red.setGeometry(QRect(237, 133, 16, 16))
        self.label_rgb_green = QLabel(Dialog)
        self.label_rgb_green.setObjectName(u"label_rgb_green")
        self.label_rgb_green.setGeometry(QRect(237, 161, 37, 12))
        self.label_rgb_blue = QLabel(Dialog)
        self.label_rgb_blue.setObjectName(u"label_rgb_blue")
        self.label_rgb_blue.setGeometry(QRect(237, 185, 37, 12))
        self.spinBox_rgb_green = QSpinBox(Dialog)
        self.spinBox_rgb_green.setObjectName(u"spinBox_rgb_green")
        self.spinBox_rgb_green.setGeometry(QRect(250, 156, 61, 21))
        self.spinBox_rgb_green.setMaximum(255)
        self.spinBox_rgb_blue = QSpinBox(Dialog)
        self.spinBox_rgb_blue.setObjectName(u"spinBox_rgb_blue")
        self.spinBox_rgb_blue.setGeometry(QRect(250, 179, 61, 21))
        self.spinBox_rgb_blue.setMaximum(255)
        self.spinBox_rgb_red = QSpinBox(Dialog)
        self.spinBox_rgb_red.setObjectName(u"spinBox_rgb_red")
        self.spinBox_rgb_red.setGeometry(QRect(250, 131, 61, 21))
        self.spinBox_rgb_red.setMaximum(255)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.checkBox_toggleLive.setText(QCoreApplication.translate("Dialog", u"Live Updates", None))
        self.label_resolution.setText(QCoreApplication.translate("Dialog", u"Resolution: 10", None))
        self.label_lineThickness.setText(QCoreApplication.translate("Dialog", u"Line thickness: 5", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Color picker", None))
        self.label_rgb_red.setText(QCoreApplication.translate("Dialog", u"R", None))
        self.label_rgb_green.setText(QCoreApplication.translate("Dialog", u"G", None))
        self.label_rgb_blue.setText(QCoreApplication.translate("Dialog", u"B", None))
    # retranslateUi

