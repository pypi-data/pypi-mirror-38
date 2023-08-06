# encoding:utf-8

import os
import re
import shutil
import sys
import zipfile

from enum import Enum
from pathlib import Path
from zipfile import ZipFile


def is_sudo():
    return os.geteuid() == 0


def remove_portable_metadata(zip_file):
    """
    Removes the dist-info folder from the zip_file to prevent it from being installed
    """
    regexs = (re.compile(r'^(?:.+?)\.dist-info/')), re.compile(r'^EGG-INFO/')
    zin = zipfile.ZipFile(zip_file, 'r')
    zout = zipfile.ZipFile(zip_file + '(1)', 'w')
    for item in zin.infolist():
        if re.search(regexs[0], item.filename) is None and re.search(regexs[1], item.filename) is None:
            buffer = zin.read(item.filename)
            zout.writestr(item, buffer)
    zout.close()
    zin.close()
    os.remove(zip_file)
    shutil.move(zip_file + '(1)', zip_file)


class ProgramType(Enum):
    INSTALLED_OR_DEVELOP = 1
    ZIP = 2
    FAKE_PORTABLE = 3


def fix_path(main_file_attr: str) -> tuple:
    """
    If this program is running from a zip file, it adds the full path of the zip file to the sys.path, instead of just a relative path
    If it's running as an installed program or a fake portable program (/temp folder), it adds the full path of the folder containing the __main__.py file to the sys.path
    If it's running from developing code, it adds the full path of the parent folder of the folder containing the __main__.py file
    :param main_file_attr: The __file__ attribute of the __main__ module
    :return: A 2-tuple containing the ProgramType and the corresponding path described above
    """
    res_type = None
    res_path = None
    main_path = os.path.realpath(main_file_attr)
    dir_candidate = os.path.dirname(main_path)
    zip_file = False if os.path.isfile(main_path) else True
    if zip_file:
        if dir_candidate not in sys.path:
            sys.path[0] = dir_candidate
        res_type = ProgramType.ZIP
        res_path = dir_candidate
    else:
        folders = [entry.name for entry in os.scandir(dir_candidate) if entry.is_dir()]
        top_package = min(folders, key=len)
        regex = re.compile(r'/tmp/{0}-\d+?/__main__\.py$'.format(top_package))
        match = re.search(regex, main_path)
        if match:
            if dir_candidate not in sys.path:
                sys.path.insert(0, dir_candidate)
            res_type = ProgramType.FAKE_PORTABLE
            res_path = dir_candidate
        else:
            root = str(Path(dir_candidate).absolute().parent)
            if root not in sys.path:
                sys.path.insert(0, root)
            res_type = ProgramType.INSTALLED_OR_DEVELOP
            res_path = root
    return res_type, res_path


def extract_single_file(zip_file, inner_file_rel_path, dst):
    with ZipFile(zip_file) as myzip:
        with myzip.open(inner_file_rel_path) as myfile, open(dst, 'wb') as destination:
            shutil.copyfileobj(myfile, destination)
