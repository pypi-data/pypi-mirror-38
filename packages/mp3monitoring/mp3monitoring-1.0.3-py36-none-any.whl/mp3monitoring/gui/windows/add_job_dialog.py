from PyQt5.QtCore import QTime, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog

from mp3monitoring.gui.windows.ui.add_job_dialog import Ui_AddJobDialog


class AddJobDialog(QDialog, Ui_AddJobDialog):
    def __init__(self, parent=None):
        super(AddJobDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        self.set_item_actions()

    def set_item_actions(self):
        self.sourceDialogButton.clicked.connect(self.source_dir_dialog)
        self.targetDialogButton.clicked.connect(self.target_dir_dialog)

    def source_dir_dialog(self):
        source_dir = QFileDialog.getExistingDirectory(self.parent(), 'Select a source directory',
                                                      options=QFileDialog.ShowDirsOnly)
        self.sourceEdit.setText(source_dir)

    def target_dir_dialog(self):
        target_dir = QFileDialog.getExistingDirectory(self.parent(), 'Select a target directory',
                                                      options=QFileDialog.ShowDirsOnly)
        self.targetEdit.setText(target_dir)

    def get_values(self):
        return self.sourceEdit.text(), self.targetEdit.text(), self.startBox.isChecked(), QTime(0, 0, 0).secsTo(
            self.pauseEdit.time())
