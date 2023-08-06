#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

__version__ = '0.2.0'

import os
import sys


def under_package_dir(package, *paths):
    if isinstance(package, str):
        import importlib
        package = importlib.import_module(package)
    p_dir = os.path.dirname(package.__file__)
    return os.path.join(p_dir, *paths)


def load_modules_under_package(package, module_names=None):
    import re
    import importlib
    if isinstance(package, str):
        package = importlib.import_module(package)
    prefix = package.__name__
    match = re.compile(r'^[^_].*\.pyc?$').match

    # by default import all modules under package
    if module_names is None:
        d = os.path.split(package.__file__)[0]
        module_names = (x for x in os.listdir(d) if match(x))
        module_names = (x.split('.')[0] for x in module_names)
        module_names = list(module_names)

    loaded = list()
    for name in module_names:
        mp = '{}.{}'.format(prefix, name)
        loaded.append(importlib.import_module(mp))
    return loaded


def under_home_dir(*paths):
    if sys.platform == 'win32':
        homedir = os.environ["HOMEPATH"]
    else:
        homedir = os.path.expanduser('~')
    return os.path.join(homedir, *paths)


def under_joker_dir(*paths):
    p = under_home_dir('.joker')
    p = os.environ.get('JOKER_HOMEDIR', p)
    p = os.path.expanduser(p)
    p = os.path.abspath(p)
    return os.path.join(p, *paths)


def make_joker_dir():
    # silently return if userdir_path exists as a dir
    d = under_joker_dir()
    if not os.path.isdir(d):
        os.mkdir(d, int('700', 8))
