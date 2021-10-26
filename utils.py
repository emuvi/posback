import os


def get_data_folder(relative_to):
    dir_path = 'data' + os.path.sep + relative_to;
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def get_data_path(relative_to, plus_name):
    return get_data_folder(relative_to) + os.path.sep + plus_name
