from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox, QMainWindow

import mp3monitoring.data.settings as settings_data
from mp3monitoring.gui.windows.ui.settings import Ui_SettingsWindow


class SettingsWindow(QMainWindow, Ui_SettingsWindow):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        self.set_item_actions()
        self.set_settings_values()

    def set_item_actions(self):
        self.dialogButtonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply_settings)
        self.dialogButtonBox.rejected.connect(self.close)

    def set_settings_values(self):
        self.guiUpdateTimeSpinBox.setValue(settings_data.GUI_UPDATE_TIME)
        self.checkForUpdatesBox.setChecked(settings_data.CHECK_UPDATE_AT_STARTUP)

    def apply_settings(self):
        settings_data.GUI_UPDATE_TIME = self.guiUpdateTimeSpinBox.value()
        settings_data.CHECK_UPDATE_AT_STARTUP = self.checkForUpdatesBox.isChecked()

        self.close()
