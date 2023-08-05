import json
from pathlib import Path

import mp3monitoring.data.settings as settings_data
import mp3monitoring.data.static as static_data


def load_settings(save_dict):
    if 'settings' in save_dict:
        settings = save_dict['settings']
        for value in static_data.SETTINGS_VALUES:
            if value.lower() in settings:
                setattr(settings_data, value, settings[value.lower()])
            else:
                print('{value} not found in settings.'.format(value=value))
    else:
        print('No settings found in save file.')


def load_save_file(path: Path):
    """
    Loads the modification times from the save file.
    :param path:
    :return: JOB_DICT, dict[file, monitor]
    """
    with path.open('r', encoding='utf-8') as reader:
        save_dict = json.load(reader)
    return save_dict


def get_settings_dict():
    settings = {}
    for value in static_data.SETTINGS_VALUES:
        try:
            settings[value.lower()] = getattr(settings_data, value)
        except AttributeError:
            print('Internal fail, for settings variable. ({variable}'.format(variable=value))
    return settings


def save_save_file(job_dict, path: Path):
    """
    Saves the modification times to the save file.
    :param job_dict: monitor jobs
    :param path:
    """
    json_dict = {'information': {'version': static_data.VERSION}, 'jobs': [], 'settings': {}}
    for job in job_dict.values():
        json_dict['jobs'].append(job.to_json_dict())

    json_dict['settings'] = get_settings_dict()

    with path.open('w', encoding='utf-8') as writer:
        json.dump(json_dict, writer, indent=4)
