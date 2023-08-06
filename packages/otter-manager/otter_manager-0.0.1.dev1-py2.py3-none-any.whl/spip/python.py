import os
import re
import sys


class Python:
    def __init__(self):
        pass


def get_python_list():
    version_pattern = re.compile(r'^[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}$')

    # pyenv
    if sys.platform == 'darwin':
        print('macOS')

        # if pyenv
        versions = os.listdir(os.path.expanduser("~/.pyenv/versions/"))
        versions = [item for item in versions if version_pattern.match(item)]

        print(versions)
