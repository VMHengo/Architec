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
    QDialogButtonBox, QLabel, QSizePolicy, QSlider,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Reset)
        self.buttonBox.setCenterButtons(False)
        self.slider_resolution = QSlider(Dialog)
        self.slider_resolution.setObjectName(u"slider_resolution")
        self.slider_resolution.setGeometry(QRect(20, 20, 160, 16))
        self.slider_resolution.setOrientation(Qt.Orientation.Horizontal)
        self.slider_lineThickness = QSlider(Dialog)
        self.slider_lineThickness.setObjectName(u"slider_lineThickness")
        self.slider_lineThickness.setGeometry(QRect(20, 60, 160, 16))
        self.slider_lineThickness.setOrientation(Qt.Orientation.Horizontal)
        self.checkBox_toggleLive = QCheckBox(Dialog)
        self.checkBox_toggleLive.setObjectName(u"checkBox_toggleLive")
        self.checkBox_toggleLive.setGeometry(QRect(30, 210, 151, 18))
        self.label_resolution = QLabel(Dialog)
        self.label_resolution.setObjectName(u"label_resolution")
        self.label_resolution.setGeometry(QRect(190, 20, 171, 16))
        self.label_lineThickness = QLabel(Dialog)
        self.label_lineThickness.setObjectName(u"label_lineThickness")
        self.label_lineThickness.setGeometry(QRect(190, 60, 181, 16))

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
    # retranslateUi

