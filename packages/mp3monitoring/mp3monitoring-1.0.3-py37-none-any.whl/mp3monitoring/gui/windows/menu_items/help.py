from functools import partial

import mp3monitoring.gui.widgets.dialogs as dialogs
from mp3monitoring.gui.windows.about import AboutWindow


def set_item_actions(parent):
    # Help -> Check for updates
    parent.actionCheckForUpdates.triggered.connect(handle_check_update)
    # Help -> About
    parent.actionAbout.triggered.connect(partial(handle_help_about, parent))


def handle_check_update():
    dialogs.information_dialog('Not implemented yet.', 'Checking for updates is not implemented yet.')


def handle_help_about(parent):
    ab = AboutWindow(parent)
    ab.show()
