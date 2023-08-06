# encoding:utf-8

import os
import shutil
import signal
import subprocess
import sys
from random import SystemRandom
from zipfile import ZipFile


def fix_path() -> str:
    zip_path = os.path.dirname(os.path.realpath(__file__))
    sys.path[0] = zip_path
    return zip_path


zip_path = fix_path()
signal.signal(signal.SIGINT, lambda x, y: None)
signal.signal(signal.SIGTERM, lambda x, y: None)


class FakePortable:
    def __init__(self):
        umask = os.umask(0)
        self.__temp_path = None
        self.__top_package = None
        self.extract_all()
        os.umask(umask)
        self.run_script()

    @property
    def temp_path(self) -> str:
        if self.__temp_path is None:
            self.__temp_path = str.format('/tmp/{0}-{1}', self.top_package, SystemRandom().getrandbits(32))
        return self.__temp_path

    @property
    def top_package(self) -> str:
        if self.__top_package is None:
            with ZipFile(zip_path) as myzip:
                files = [file for file in myzip.namelist() if file.count('/')]
                top = min(files, key=len)
                self.__top_package = top.split('/')[0]
        return self.__top_package

    def extract_all(self):
        os.makedirs(self.temp_path, exist_ok=True)
        with ZipFile(zip_path) as myzip:
            myzip.extractall(self.temp_path)
        os.remove(self.temp_path + '/__main__.py')
        shutil.move(self.temp_path + '/__main2__.py', self.temp_path + '/__main__.py')

    def run_script(self):
        args = ' '.join(sys.argv[1:])
        subprocess.run(['python3 {0} {1}'.format(self.temp_path + '/__main__.py', args)], shell=True)
        shutil.rmtree(self.temp_path, ignore_errors=True)
        sys.exit(0)


f = FakePortable()
