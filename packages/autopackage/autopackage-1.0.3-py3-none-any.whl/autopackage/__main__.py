#!/usr/bin/env python3
# encoding:utf-8

import glob
import os
import re
import shutil

from setuptools import setup

from autopackage.parsers.autoparser import autoparse
from autopackage.parsers.setup_parser import MainModuleLocation, move_main_module
from autopackage.program.statics import Statics
from autopackage.utils.utils import extract_single_file, remove_portable_metadata

Statics.set_autopack_dir(__file__)


def main():
    autoparser = autoparse()

    # If the program to be packaged is a fake portable
    if autoparser.fake_portable:
        move_main_module(MainModuleLocation.INSIDE, MainModuleLocation.TOP)
        Statics.PROGRAM_CONFIG.py_modules = ('__main__', '__main2__')
        shutil.move(Statics.SETUP_DIR + '/__main__.py', Statics.SETUP_DIR + '/__main2__.py')

        # If autopackage is running from a zip file
        if Statics.IS_ZIP:
            extract_single_file(Statics.AUTOPACK_DIR, Statics.FAKE_PORTABLE_MODULE_PATH, Statics.SETUP_DIR + '/__main__.py')

        # Then, it can be running either from a fake portable path or an installed location
        else:
            shutil.copyfile(Statics.AUTOPACK_DIR + '/' + Statics.FAKE_PORTABLE_MODULE_PATH, Statics.SETUP_DIR + '/__main__.py')

    # If the program to be packaged is portable
    elif autoparser.portable:
        move_main_module(MainModuleLocation.INSIDE, MainModuleLocation.TOP)
        Statics.PROGRAM_CONFIG.py_modules = ('__main__',)

    # If it's not portable, then it's installable
    try:
        setup(
            name=Statics.PROGRAM_CONFIG.name,
            version=Statics.PROGRAM_CONFIG.version,
            description=Statics.PROGRAM_CONFIG.description,
            long_description=Statics.PROGRAM_CONFIG.long_description,
            author=Statics.PROGRAM_CONFIG.author,
            author_email=Statics.PROGRAM_CONFIG.author_email,
            maintainer=Statics.PROGRAM_CONFIG.maintainer,
            maintainer_email=Statics.PROGRAM_CONFIG.maintainer_email,
            url=Statics.PROGRAM_CONFIG.url,
            download_url=Statics.PROGRAM_CONFIG.download_url,
            license=Statics.PROGRAM_CONFIG.license,
            keywords=Statics.PROGRAM_CONFIG.keywords,
            packages=Statics.PROGRAM_CONFIG.packages,
            py_modules=Statics.PROGRAM_CONFIG.py_modules,
            zip_safe=Statics.PROGRAM_CONFIG.zip_safe,
            classifiers=Statics.PROGRAM_CONFIG.classifiers,
            platforms=Statics.PROGRAM_CONFIG.platforms,
            entry_points=Statics.PROGRAM_CONFIG.entry_points,
            install_requires=Statics.PROGRAM_CONFIG.install_requires,
            python_requires=Statics.PROGRAM_CONFIG.python_requires,
            package_data=Statics.PROGRAM_CONFIG.package_data,
            data_files=Statics.PROGRAM_CONFIG.data_files,
        )

    except SystemExit as sysexit:
        print(sysexit.args[0])

    # We create the releases folder if it doesn't exist and we look for the newly created file
    os.makedirs(Statics.RELEASES_DIR, exist_ok=True)
    created_pkg = glob.glob(Statics.SETUP_DIR + '/dist/*')

    # We make sure the package has been created
    if len(created_pkg) != 0:
        created_pkg = created_pkg[0]

        if autoparser.fake_portable:
            os.remove(Statics.SETUP_DIR + '/__main__.py')
            shutil.move(Statics.SETUP_DIR + '/__main2__.py', Statics.SETUP_DIR + '/__main__.py')

        if autoparser.portable:
            # We remove the extension and the package metadata
            new_name = created_pkg[:-4]
            created_pkg = shutil.move(created_pkg, new_name)
            remove_portable_metadata(created_pkg)

            # We add the execution header
            print('setting execution permissions to file ' + os.path.basename(created_pkg))
            os.system(str.format("echo '#!/usr/bin/env python3' | cat - {0} > temp && mv temp {0} ; chmod +x {0}", re.escape(created_pkg)))

        # We move the package to the releases folder, overwriting any other file with the same name if necessary
        created_pkg = os.path.basename(created_pkg)
        if os.path.exists(Statics.RELEASES_DIR + created_pkg):
            os.remove(Statics.RELEASES_DIR + created_pkg)
        shutil.move(Statics.SETUP_DIR + '/dist/' + created_pkg, Statics.RELEASES_DIR)

    # We put the __main__ module back in its package and we remove all the folders created during the packaging process
    if autoparser.portable:
        move_main_module(MainModuleLocation.TOP, MainModuleLocation.INSIDE)
    shutil.rmtree(Statics.SETUP_DIR + '/build/', ignore_errors=True)
    shutil.rmtree(Statics.SETUP_DIR + '/dist/', ignore_errors=True)
    egg_info_dir = glob.glob(Statics.SETUP_DIR + '/*.egg-info')
    if len(egg_info_dir) != 0:
        shutil.rmtree(egg_info_dir[0], ignore_errors=True)


if __name__ == '__main__':
    main()
