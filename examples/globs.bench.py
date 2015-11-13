from minibench import Benchmark

import fnmatch
import os
import re
import tempfile

from glob import iglob


class BenchmarkGlobs(Benchmark):
    '''
    Glob benchmark

    See: http://www.reddit.com/r/Python/comments/de2xp/dae_need_this_in_a_lot_of_projects/c0zj813?context=3
    '''
    def before_class(self):
        self.walk_root = tempfile.gettempdir()
        for i in range(0, 100):
            tempfile.mkstemp(suffix=".txt")

    def bench_glob(self):
        items = []
        for root, dirs, files in os.walk(self.walk_root):
            for item in iglob(os.path.join(root, '*.txt')):
                items.append(item)

    def bench_fnmatch(self):
        items = []
        for root, dirs, files in os.walk(self.walk_root):
            for item in fnmatch.filter(files, '*.txt'):
                items.append(os.path.join(root, item))

    def bench_re(self):
        items = []
        rex = re.compile(".*\.txt$")
        for root, dirs, files in os.walk(self.walk_root):
            for item in files:
                if rex.match(item):
                    items.append(os.path.join(root, item))
