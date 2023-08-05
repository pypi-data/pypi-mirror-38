from functools import partial

from mp3monitoring.gui.windows.settings import SettingsWindow


def set_item_actions(parent):
    parent.actionSettings.triggered.connect(partial(handle_settings_settings, parent))


def handle_settings_settings(parent):
    sw = SettingsWindow(parent)
    sw.show()
