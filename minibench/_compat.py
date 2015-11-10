# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from glob import glob

from six import string_types  # noqa


def load_module(name, filename):
    '''Load a module into name given its filename'''
    if sys.version_info < (3, 5):
        import imp
        import warnings
        with warnings.catch_warnings():  # Required for Python 2.7
            warnings.simplefilter("ignore", RuntimeWarning)
            return imp.load_source(name, filename)
    else:
        from importlib.machinery import SourceFileLoader
        loader = SourceFileLoader(name, filename)
        return loader.load_module()


def recursive_glob(pattern):
    if sys.version_info < (3, 5):
        if '/**/' in pattern:
            import fnmatch
            import os
            matches = []
            prefix, pattern = pattern.split('**/')
            for root, dirnames, filenames in os.walk(prefix):
                for filename in fnmatch.filter(filenames, pattern):
                    matches.append(os.path.join(root, filename))
            return matches

        return glob(pattern)
    else:
        return glob(pattern, recursive=True)
