from functools import partial

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

import mp3monitoring.data.dynamic as dynamic_data

remover_dict = {}  # dictionary which contains the object and thread who removes the monitor threads


class StopMonitorWorker(QObject):
    finished = pyqtSignal()

    @pyqtSlot(name='remove_monitor')
    def remove(self, source_dir):
        stop_monitor(source_dir)
        self.finished.emit()


def add_remover(source_dir, model):
    global remover_dict
    stopper = StopMonitorWorker()
    stop_thread = QThread()
    stopper.moveToThread(stop_thread)
    stop_thread.started.connect(partial(stopper.remove, source_dir))
    stopper.finished.connect(partial(remove_worker, source_dir))
    stopper.finished.connect(model.update_model)
    remover_dict[source_dir] = (stop_thread, stopper)
    stop_thread.start()


def stop_monitor(source):
    monitor = dynamic_data.JOB_DICT[source]
    monitor.stop()
    if monitor.thread.is_alive():
        monitor.thread.join()
    del dynamic_data.JOB_DICT[source]


def remove_worker(source_dir):
    global remover_dict
    remover_dict[source_dir][0].quit()
    remover_dict[source_dir][0].wait()
    del remover_dict[source_dir]
