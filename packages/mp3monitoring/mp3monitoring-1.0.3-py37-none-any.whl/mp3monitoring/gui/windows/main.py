from functools import partial

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialogButtonBox, QHeaderView, QMainWindow, QMenu, QSystemTrayIcon

from mp3monitoring.gui.check_box import CheckBoxDelegate
from mp3monitoring.gui.data import dynamic as dynamic_gui_data
from mp3monitoring.gui.data import monitor_table_view
from mp3monitoring.gui.data.monitor_table_model import DataTableModel
from mp3monitoring.gui.widgets import dialogs
from mp3monitoring.gui.widgets.shutdown_overlay import ShutdownOverlay
from mp3monitoring.gui.windows import menu_items
from mp3monitoring.gui.windows.ui.main import Ui_MainWindow
from mp3monitoring.gui.workers.shutdown_worker import ShutdownWorker


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.app = app

        # set icon
        icon = QIcon()
        icon.addPixmap(QPixmap(dynamic_gui_data.ICON_FILE), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # menu items
        menu_items.file.set_item_actions(self)
        menu_items.settings.set_item_actions(self)
        menu_items.help.set_item_actions(self)

        # shutdown overlay
        self.overlay = ShutdownOverlay(self)
        self.gridLayout.addWidget(self.overlay, 0, 0, 1, 1)
        self.overlay.hide()

        # tray icon
        self.tray_icon = None
        self.create_tray_icon()

        # init shutdown thread
        self.shutdown_worker = ShutdownWorker()
        self.shutdown_thread = QThread()
        self.shutdown_worker.status.connect(lambda msg: self.change_status_bar(msg))
        self.shutdown_worker.finished.connect(self.app.quit)
        self.shutdown_worker.moveToThread(self.shutdown_thread)
        self.shutdown_thread.started.connect(self.shutdown_worker.shutdown)

        # create monitor table
        self.create_monitor_table()

        # add context menu to table view
        self.monitorTableView.customContextMenuRequested.connect(
            partial(monitor_table_view.context_menu, self.monitorTableView))

    def change_status_bar(self, msg, time=5000):
        self.statusBar.showMessage(msg, time)

    def closeEvent(self, event, close_immediately=False):  # TODO
        event.ignore()
        if not QSystemTrayIcon.isSystemTrayAvailable():
            value = dialogs.question_dialog('Exiting...', 'Do you really want to exit?')
            if bool(value & QDialogButtonBox.Yes):
                self.exit()
        else:
            self.tray_icon.show()
            self.hide()
            if QSystemTrayIcon.supportsMessages():
                self.tray_icon.showMessage("MP3 Monitoring is running in background!",
                                           "Double click tray icon to open window and right click for menu.")

    def exit(self):  # TODO: deactivate close button
        self.menuBar.setEnabled(False)
        self.overlay.show()
        self.show_window()

        self.shutdown_thread.start()

    def create_tray_icon(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(dynamic_gui_data.ICON_FILE), QIcon.Normal, QIcon.Off)
        self.tray_icon = QSystemTrayIcon(icon)
        self.tray_icon.activated.connect(self.tray_icon_clicked)

        menu = QMenu(self)
        open_action = menu.addAction("Open")
        menu.addSeparator()
        exit_action = menu.addAction("Exit")
        open_action.triggered.connect(self.show_window)
        exit_action.triggered.connect(self.exit)
        self.tray_icon.setContextMenu(menu)

    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
        elif reason == QSystemTrayIcon.Context:
            pass  # context menu automatically shown by the system tray icon

    def show_window(self):
        self.show()
        self.tray_icon.hide()

    def create_monitor_table(self):
        header = [' active ', ' source ', ' target ', ' status ', ' pause (s) ']
        table_model = DataTableModel(header, self)
        self.monitorTableView.setModel(table_model)
        self.monitorTableView.setSortingEnabled(False)  # TODO

        self.monitorTableView.setItemDelegateForColumn(0, CheckBoxDelegate(self.monitorTableView))

        h_header = self.monitorTableView.horizontalHeader()
        h_header.setSectionResizeMode(0, QHeaderView.Fixed)  # active
        h_header.setSectionResizeMode(1, QHeaderView.Stretch)  # source dir
        h_header.setSectionResizeMode(2, QHeaderView.Stretch)  # target dir
        self.monitorTableView.resizeColumnsToContents()
