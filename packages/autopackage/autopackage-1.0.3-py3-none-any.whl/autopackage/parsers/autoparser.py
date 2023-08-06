# encoding:utf-8

import os
import runpy
import sys
from argparse import ArgumentParser, FileType, SUPPRESS

from autopackage.program.statics import Statics


class AutoParser:
    def __init__(self):
        self.portable = None
        self.help = None
        self.setup = None
        self.fake_portable = None

        parser = ArgumentParser(description='Autopackage Help', add_help=False, usage=SUPPRESS)
        parser.add_argument('-p', '--portable', action='store_true', default=False, help='Define whether the program should be packaged as portable')
        parser.add_argument('-s', '--setup', type=FileType('r'), help='The setup.py file of the project to be packaged')
        parser.add_argument('-h', '--help', action='store_true', default=False, help='Show this help')
        args, resto = vars(parser.parse_known_args()[0]), parser.parse_known_args()[1]
        self.parse_args(args)
        self.run(parser)

    def parse_args(self, args):
        self.help = args['help']
        self.portable = args['portable']
        self.setup = args['setup']

    def run(self, parser):
        if self.help or not self.setup:
            parser.print_help()
            print('\n---------------------------------------------------------------------\n')
            sys.exit(0)
        elif self.setup:
            Statics.SETUP_MODULE = os.path.realpath(self.setup.name)
            Statics.SETUP_DIR = os.path.dirname(Statics.SETUP_MODULE)
            Statics.RELEASES_DIR = Statics.SETUP_DIR + '/releases/'
            os.chdir(Statics.SETUP_DIR)  # This is what makes the find_packages() function of the setup.py module work correctly
            runpy.run_path(Statics.SETUP_MODULE, run_name=Statics.SETUP_MODULE)
            sys.argv = [Statics.SETUP_MODULE, 'bdist_wheel']


def autoparse():
    autoparser = AutoParser()
    Statics.MAIN_PATH = Statics.SETUP_DIR + '/' + Statics.PROGRAM_CONFIG.top_package + '/__main__.py'
    autoparser.fake_portable = True if (autoparser.portable and not Statics.PROGRAM_CONFIG.zip_safe) else False
    return autoparser
