# utils.py

import os

def get_sources_dir(dirs: list):
    for d in dirs:
        if os.path.isdir(d):
            return d
    return None
