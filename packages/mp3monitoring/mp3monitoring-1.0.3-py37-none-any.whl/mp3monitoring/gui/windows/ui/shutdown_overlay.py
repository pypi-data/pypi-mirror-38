# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shutdown_overlay.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ShutdownOverlay(object):
    def setupUi(self, ShutdownOverlay):
        ShutdownOverlay.setObjectName("ShutdownOverlay")
        ShutdownOverlay.resize(598, 379)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ShutdownOverlay.sizePolicy().hasHeightForWidth())
        ShutdownOverlay.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Noto Sans UI")
        ShutdownOverlay.setFont(font)
        ShutdownOverlay.setWindowOpacity(1.0)
        ShutdownOverlay.setAutoFillBackground(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(ShutdownOverlay)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 95, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.indicator = RotatingIndicator(ShutdownOverlay)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.indicator.sizePolicy().hasHeightForWidth())
        self.indicator.setSizePolicy(sizePolicy)
        self.indicator.setObjectName("indicator")
        self.gridLayout = QtWidgets.QGridLayout(self.indicator)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout.addWidget(self.indicator)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.message = QtWidgets.QLabel(ShutdownOverlay)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.message.sizePolicy().hasHeightForWidth())
        self.message.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Noto Sans UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.message.setFont(font)
        self.message.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.message.setLineWidth(0)
        self.message.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.message.setObjectName("message")
        self.verticalLayout.addWidget(self.message, 0, QtCore.Qt.AlignHCenter)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(ShutdownOverlay)
        QtCore.QMetaObject.connectSlotsByName(ShutdownOverlay)

    def retranslateUi(self, ShutdownOverlay):
        _translate = QtCore.QCoreApplication.translate
        ShutdownOverlay.setWindowTitle(_translate("ShutdownOverlay", "Form"))
        self.message.setText(_translate("ShutdownOverlay", "Exiting..."))

from mp3monitoring.gui.widgets.rotating_indicator import RotatingIndicator
