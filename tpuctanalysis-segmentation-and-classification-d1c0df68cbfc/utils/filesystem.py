import os


def create_dirs(dir_path_names, remove_old=False):
    """
    Creates directory by the path
    :param dir_path_names: List of paths to directories to create
    :param remove_old: Whether to delete old one directory with the same path name
    """
    for dp in dir_path_names:
        if not os.path.exists(dp):
            os.makedirs(dp)
        elif remove_old:
            remove_dir(dir_path_names)


def remove_dir(dir_path):
    """
    Removes the directory from the filesystem
    :param dir_path: Path to the directory to remove
    """
    if os.path.exists(dir_path):
        entries = sorted(os.listdir(dir_path))
        for entry in entries:
            entry_path = os.path.join(dir_path, entry)
            if os.path.isdir(entry_path):
                remove_dir(entry_path)
            else:
                os.remove(entry_path)

        try:
            os.removedirs(dir_path)
        except Exception as e:
            pass
