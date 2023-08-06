#/usr/bin/env python
import os

from . import Application

HOME_DIR = os.environ.get('HOME')
CONFIG = os.path.join(HOME_DIR, '.dictionaryapi/config')

if __name__ == '__main__':
    print('app')
