#!/usr/bin/env python

import os
import json
from setuptools import setup

# Default version number
BASE_VERSION = '0.0.0'
METADATA_FILENAME = 'cloudmanager_notebook/package_metadata.json'
BASEPATH = os.path.dirname(os.path.abspath(__file__))
METADATA_FILE = os.path.join(BASEPATH, METADATA_FILENAME)

def readme():
    """
    Get the contents of the README file
    :return:
    """
    possible_filenames = ['README.rst', 'README.md', 'README.txt']
    filename = None
    data = ''
    for filename in possible_filenames:
        if os.path.exists(filename):
            break
    if filename:
        with open(filename) as file_handle:
            data = file_handle.read()
    return data


def scripts():
    """
    Get a list of the scripts in the scripts directory

    Returns
    -------
    list
        A list of strings containing the scripts in the scripts directory
    """
    script_list = []

    if os.path.isdir('scripts'):
        script_list += [
            os.path.join('scripts', f) for f in os.listdir('scripts')
        ]
    return script_list


def get_version(version_file):
    """
    Get the version number based on the BUILD_NUMBER

    Parameters
    ----------
    version_file : str
        The python file to store the version metadata in

    Returns
    -------
    str
        Version string
    """
    for env_variable in ['BUILD_NUMBER', 'TRAVIS_BUILD_NUMBER']:
        build_number = int(os.environ.get(env_variable, '3'))
        if build_number:
            break

    version = BASE_VERSION.split('.')
    version[-1] = str(build_number)
    version = '.'.join(version)
    if build_number != 0:
        with open(version_file, 'w') as version_handle:
            json.dump({'version': version}, version_handle)

    elif os.path.exists(version_file):
        with open(version_file) as version_handle:
            version = json.load(version_handle)['version']

    return version


if __name__ == '__main__':
    version = get_version(BASE_VERSION)
    setup(
        name='cloudmanager-notebook',
        version=get_version(METADATA_FILENAME),
        author='Dwight Hubbard',
        author_email='dhubbard',
        extras_require={
            'esp8266': 'cloudmanager-micropython-esp8266'
        },
        url='http=//github.com/dhubbard/cloudmanager-notebook',
        license='LICENSE.txt',
        packages=[
            'cloudmanager_notebook', 'cloudmanager_notebook_ui',
        ],
        long_description='Short description of this project',
        description='Short description of this project',
        install_requires=[
            'Django<=1.10', 'Jinja2', 'micropython-cloudmanager'
        ],
        package_data= {
            'cloudmanager_notebook_ui': [
                'package_metadata.json',
                'fixtures/*',
                'static/backgrounds/*',
                'static/css/*',
                'static/fonts/*',
                'static/js/*',
                'static/lib/*',
                'static/logos/*',
                'static/mode/*',
                'static/mode/python/*',
                'static/cloudmanager_notebook_ui/*',
                'static/cloudmanager_notebook_ui/js/*',
                'static/cloudmanager_notebook_ui/lib/*',
                'static/cloudmanager_notebook_ui/mode/*',
                'static/cloudmanager_notebook_ui/mode/python/*',
                'templates/*',
                'templates/cloudmanager_notebook_ui/*',
            ],
        },
        scripts= scripts()
    )
