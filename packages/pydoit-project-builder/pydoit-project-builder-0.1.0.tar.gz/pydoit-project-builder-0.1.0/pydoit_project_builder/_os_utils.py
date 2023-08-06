"""Define tasks."""
import os
from shutil import rmtree


def create_dir(directory):
    """Create a directory and if needed parents."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return True


def remove_directories(list_dir):
    """Remove every directories from a list."""
    for folder in list_dir:
        rmtree(folder, ignore_errors=True)


def remove_files(list_files):
    """Remove every files from a list."""
    for f in list_files:
        if os.path.exists(f):
            os.remove(f)


def is_windows():
    """Return true if the running machine is on windows."""
    return os.name == "nt"
