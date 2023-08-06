# encoding:utf-8

import os
import shutil
from enum import Enum
from shutil import SameFileError

from autopackage.program.statics import Statics


class SetupParser:
    def __init__(self, name, version, author, packages, license, keywords, classifiers, author_email='', description='', long_description='', maintainer='', maintainer_email='', platforms=('any',),
                 url='', download_url='', py_modules=(), zip_safe=False, entry_points=(), install_requires=(), python_requires='', package_data={}, data_files=()):
        self.name = name
        self.version = version
        self.author = author
        self.author_email = author_email
        self.maintainer = maintainer
        self.maintainer_email = maintainer_email
        self.license = license
        self.keywords = keywords
        self.classifiers = classifiers
        self.platforms = platforms
        self.description = description
        self.long_description = long_description
        self.url = url
        self.download_url = download_url
        self.packages = packages
        self.py_modules = py_modules
        self.zip_safe = zip_safe
        self.entry_points = entry_points
        self.install_requires = install_requires
        self.python_requires = python_requires
        self.package_data = package_data
        self.data_files = data_files
        self.top_package = min(self.packages, key=len)
        Statics.PROGRAM_CONFIG = self


class MainModuleLocation(Enum):
    INSIDE = 1
    TOP = 2


def move_main_module(src: MainModuleLocation, dst: MainModuleLocation):
    """
    Moves the main module to the selected location.
    """
    top_path = Statics.SETUP_DIR + '/__main__.py'
    if src == dst:
        raise SameFileError('Error: src and dst cannot be the same')
    src = top_path if src is MainModuleLocation.TOP else Statics.MAIN_PATH
    dst = top_path if dst is MainModuleLocation.TOP else Statics.MAIN_PATH
    if os.path.isfile(src):
        shutil.move(src, dst)
    else:
        raise FileNotFoundError('File {0} not found'.format(src))
