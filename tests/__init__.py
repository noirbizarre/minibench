# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import join, abspath

EXAMPLES = abspath(join(__name__, '..', 'examples'))


class ModuleFactory(object):
    def __init__(self, *benchmarks):
        for benchmark in benchmarks:
            setattr(self, benchmark.__name__, benchmark)
