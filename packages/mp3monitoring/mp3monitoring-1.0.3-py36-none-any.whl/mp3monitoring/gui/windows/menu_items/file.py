from functools import partial
from pathlib import Path

from PyQt5.QtWidgets import QDialog

from mp3monitoring.gui.widgets.dialogs import information_dialog
from mp3monitoring.gui.windows.add_job_dialog import AddJobDialog
from mp3monitoring.monitor import Monitor, add_new_monitor


def set_item_actions(parent):
    # File -> Add...
    parent.actionAdd.triggered.connect(partial(handle_file_add, parent))
    # File -> Exit
    parent.actionExit.triggered.connect(parent.exit)


def handle_file_add(parent):
    """
    Can load ONLY offline profiles at the moment.
    :return:
    """
    dialog = AddJobDialog(parent)
    state = dialog.exec()
    if state == QDialog.Accepted:
        values = dialog.get_values()
        if values[0] == '' or values[1] == '':
            information_dialog('Could not create monitor job.', 'Source or target directory value was empty.')
            return
        add_new_monitor(Monitor(Path(values[0]), Path(values[1]), values[2], pause=values[3]))
