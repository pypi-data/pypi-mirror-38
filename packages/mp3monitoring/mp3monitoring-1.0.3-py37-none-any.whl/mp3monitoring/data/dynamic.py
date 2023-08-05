"""
Data which will be generated while starting and should be available global.
"""
from pathlib import Path

import mp3monitoring.data.static as static_data

SAVE_FILE = Path.home().joinpath('.' + static_data.NAME.replace(' ', '_')).joinpath('data.sav')
JOB_DICT = {}
DISABLE_TQDM = False
