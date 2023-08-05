import shutil
import time
import traceback
from pathlib import Path
from threading import Thread

import mutagen.mp3
from tqdm import tqdm

from mp3monitoring.data import dynamic as dynamic_data


class Monitor:
    def __init__(self, source_dir: Path, target_dir: Path, start, pause=10, last_mod_time=0):
        """
        :param source_dir: source directory
        :param target_dir: target directory
        :param start:
        :param pause: pause in seconds between the scans
        :param last_mod_time: last modification time
        """
        super().__init__()
        self.startup = start
        self.status = 'Initialization'
        self.source_dir = source_dir.resolve()
        self.target_dir = target_dir.resolve()
        self.last_mod_time = last_mod_time
        self.__sleep_time = 1
        self.pause = pause
        self.change_pause(pause)

        self.stopping = not start
        self.thread = Thread(target=self.__run)

        self.status = 'Stopped'
        self.check_directories()

    @classmethod
    def from_json_dict(cls, json_dict):
        source_dir = Path(json_dict['source_dir'])
        target_dir = Path(json_dict['target_dir'])
        startup = json_dict['startup']
        pause = json_dict['pause']
        last_mod_time = json_dict['last_mod_time']
        return cls(source_dir, target_dir, startup, pause, last_mod_time)

    def __str__(self):
        return "{active} | {source} | {target} | {pause}s | {status} | {startup} | {time}".format(
            active=self.thread.isAlive(),
            source=str(self.source_dir),
            target=str(self.target_dir),
            pause=str(self.pause),
            status=self.status,
            startup=self.startup,
            time=self.last_mod_time)

    def start(self):
        """

        :return:
        """
        self.status = 'Starting'
        if not self.check_directories():
            self.stopping = True
            return False
        self.stopping = False
        self.thread = Thread(target=self.__run)
        self.thread.start()
        return True

    def stop(self):
        self.status = 'Stopping'
        self.stopping = True

    def __run(self):
        """
        Scans a source directory every pause_s seconds, for new mp3 and copies them to the target directory.
        Warning: excepts KeyboardInterrupt!
        :return: last_mod_time
        """
        try:
            while not self.stopping:
                self.status = 'Checking for modifications'
                new_mod_time = time.time()
                new_mod_files = get_all_files_after_time(self.source_dir, after_time=self.last_mod_time)
                if new_mod_files:
                    self.status = 'Checking for mp3'
                    mp3_files = get_all_mp3(new_mod_files)
                    # del mp3_files
                    if mp3_files:
                        self.status = 'Copying new mp3'
                        copy_files(mp3_files, self.target_dir)
                self.last_mod_time = new_mod_time
                self.status = 'Sleeping'
                cur_sleep = 0
                while cur_sleep < self.pause:
                    time.sleep(self.__sleep_time)
                    if self.stopping:  # dont sleep more, go to while loop check
                        break
                    cur_sleep += self.__sleep_time
        except KeyboardInterrupt:
            pass
        self.status = 'Stopped'

    def check_directories(self):
        """
        Check source and initialize target directory.
        """
        if not self.source_dir.exists():
            self.status = 'Source ({source_dir}) does not exist.'.format(source_dir=str(self.source_dir))
            return False
        elif not self.source_dir.is_dir():
            self.status = 'Source ({source_dir}) is not a directory.'.format(source_dir=str(self.source_dir))
            return False

        if not self.target_dir.exists():
            try:
                Path.mkdir(self.target_dir, parents=True)
            except PermissionError:
                self.status = 'Cant create target directory ({target_dir}). Do you have write permissions?'.format(
                    target_dir=str(self.target_dir))
            return False
        elif not self.target_dir.is_dir():
            self.status = 'Target ({target_dir}) is not a directory.'.format(target_dir=str(self.target_dir))
            return False
        return True

    def change_pause(self, pause):
        if pause < 0:
            pause = 0
        self.pause = pause
        if pause > 10 and pause % 10 == 0:
            self.__sleep_time = 10
        else:
            self.__sleep_time = 1

    def to_json_dict(self):
        return {'source_dir': str(self.source_dir),
                'target_dir': str(self.target_dir),
                'pause': self.pause,
                'startup': self.startup,
                'last_mod_time': self.last_mod_time
                }


def add_new_monitor(monitor):
    dynamic_data.JOB_DICT[str(monitor.source_dir)] = monitor
    if monitor.startup:
        if not monitor.start():
            monitor.startup = False
            print(monitor, monitor.status)


def get_all_files_after_time(directory, after_time=0):
    """
    Check all files in the given directory if access or creation time after the given time.
    :param directory: directory which will be checked
    :param after_time: time in seconds (unixtime)
    :return: list of modified/created files after time
    """
    files = directory.glob('**/*')
    return [file for file in files if
            (file.is_file() and (max(file.stat().st_mtime, file.stat().st_ctime) > after_time))]


def is_mp3(file_path: Path):
    """
    Check a file for mp3 and if its a valid MPEG audio format.
    :param file_path: file to be checked
    :return: if its can be loaded as mp3 and if its a valid MPEG format.
    """
    try:
        return not mutagen.mp3.MP3(str(file_path)).info.sketchy
    except mutagen.mp3.HeaderNotFoundError:
        pass
    except FileNotFoundError:
        pass
    return False


def get_all_mp3(files):
    """
    Checks the files list for mp3.
    :param files: file list
    :return: set(file)
    """
    pbar = tqdm(files, desc="Checking for mp3", unit="file", leave=True, mininterval=0.2, ncols=100, disable=dynamic_data.DISABLE_TQDM)
    mp3_files = {file for file in pbar if is_mp3(file)}
    pbar.close()
    return mp3_files


def copy_files(files, target_dir: Path):
    """
    Copy given file list to target directory.
    :param files: set(file)
    :param target_dir: target directory
    :param pbar:
    :return:
    """
    pbar = tqdm(files, desc="Copying new mp3", unit="mp3", leave=True, mininterval=0.2, ncols=100, disable=dynamic_data.DISABLE_TQDM)
    for file in pbar:
        try:
            new_file = target_dir.joinpath(file.name)
            new_file = new_file.with_suffix('.mp3')

            while new_file.exists():
                new_file = new_file.with_name(new_file.stem + '_d.mp3')

            shutil.copy2(str(file), str(target_dir))
            target_dir.joinpath(file.name).rename(new_file)
        except Exception:
            pbar.write('Couldnt copy ' + str(file))
            traceback.print_exc()
    pbar.refresh()
    pbar.close()
