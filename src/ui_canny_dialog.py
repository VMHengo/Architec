# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'canny_dialog.ui'
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
    QDialogButtonBox, QLabel, QSizePolicy, QSlider,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(316, 207)
        self.slider_upperThresh = QSlider(Dialog)
        self.slider_upperThresh.setObjectName(u"slider_upperThresh")
        self.slider_upperThresh.setGeometry(QRect(20, 25, 160, 16))
        self.slider_upperThresh.setMaximum(300)
        self.slider_upperThresh.setValue(150)
        self.slider_upperThresh.setOrientation(Qt.Orientation.Horizontal)
        self.slider_lowerThresh = QSlider(Dialog)
        self.slider_lowerThresh.setObjectName(u"slider_lowerThresh")
        self.slider_lowerThresh.setGeometry(QRect(20, 70, 161, 31))
        self.slider_lowerThresh.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.slider_lowerThresh.setValue(50)
        self.slider_lowerThresh.setOrientation(Qt.Orientation.Horizontal)
        self.label_upperText = QLabel(Dialog)
        self.label_upperText.setObjectName(u"label_upperText")
        self.label_upperText.setGeometry(QRect(10, 10, 141, 16))
        self.label_lowerText = QLabel(Dialog)
        self.label_lowerText.setObjectName(u"label_lowerText")
        self.label_lowerText.setGeometry(QRect(10, 60, 121, 16))
        self.label_upper = QLabel(Dialog)
        self.label_upper.setObjectName(u"label_upper")
        self.label_upper.setGeometry(QRect(190, 23, 101, 16))
        self.label_lower = QLabel(Dialog)
        self.label_lower.setObjectName(u"label_lower")
        self.label_lower.setGeometry(QRect(190, 80, 71, 16))
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(100, 160, 164, 18))
        self.buttonBox.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Reset)
        self.checkBox_toggleLive = QCheckBox(Dialog)
        self.checkBox_toggleLive.setObjectName(u"checkBox_toggleLive")
        self.checkBox_toggleLive.setGeometry(QRect(10, 100, 111, 18))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_upperText.setText(QCoreApplication.translate("Dialog", u"upper threshold", None))
        self.label_lowerText.setText(QCoreApplication.translate("Dialog", u"lower threshold", None))
        self.label_upper.setText(QCoreApplication.translate("Dialog", u"Threshold: 150", None))
        self.label_lower.setText(QCoreApplication.translate("Dialog", u"Threshold: 50", None))
        self.checkBox_toggleLive.setText(QCoreApplication.translate("Dialog", u"Live Updates", None))
    # retranslateUi

