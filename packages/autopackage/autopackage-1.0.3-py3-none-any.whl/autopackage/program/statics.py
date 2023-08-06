# encoding:utf-8

import os

from autopackage.utils.utils import fix_path, ProgramType


class Statics:
    AUTOPACK_DIR = None  # The absolute path to the running zip file, the fake portable running folder or the installed folder. Never ends with '/' .
    IS_FAKE_PORTABLE = None  # autopackage is running as a fake portable (temp folder)
    IS_ZIP = False if os.path.isfile(os.path.realpath(__file__)) else True  # autopackage is running from a zip file
    FAKE_PORTABLE_MODULE_PATH = 'autopackage/program/fake_portable.py'
    SETUP_MODULE = None
    SETUP_DIR = None
    MAIN_PATH = None
    PROGRAM_CONFIG = None
    RELEASES_DIR = None

    @classmethod
    def set_autopack_dir(cls, main_file_attr):
        programtype, path = fix_path(main_file_attr)
        cls.AUTOPACK_DIR = path
        cls.IS_FAKE_PORTABLE = True if programtype is ProgramType.FAKE_PORTABLE else False
