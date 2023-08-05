from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from mp3monitoring.gui.data import dynamic as dynamic_gui_data


def question_dialog(win_msg, msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowIcon(QIcon(dynamic_gui_data.ICON_FILE))

    msg_box.setText(msg)
    msg_box.setWindowTitle(win_msg)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    reply = msg_box.exec()
    return reply


def information_dialog(win_msg, msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowIcon(QIcon(dynamic_gui_data.ICON_FILE))

    msg_box.setText(msg)
    msg_box.setWindowTitle(win_msg)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()
