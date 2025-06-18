# import os
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'assets'))
# DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))

import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Для собранного приложения PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.join(base_dir, relative_path)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = resource_path('assets')
DATA_DIR = resource_path('data')



