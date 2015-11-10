from minibench import Benchmark

import random
from operator import itemgetter


def fnouter(x):
    return x[1]


class SortDictByValue(Benchmark):
    '''
    Sort Dict with 100 Keys by Value

    See: http://writeonly.wordpress.com/2008/08/30/sorting-dictionaries-by-value-in-python-improved/
    '''
    times = 10000

    def before_class(self):
        self.d = dict(zip(range(100), range(100)))

    def each_each(self):
        random.shuffle(self.d)

    def bench_pep265(self):
        return sorted(self.d.items(), key=itemgetter(1))

    def bench_stupid(self):
        return [(k, v) for v, k in sorted([(v, k) for k, v in self.d.items()])]

    def bench_listExpansion(self):
        L = [(k, v) for (k, v) in self.d.items()]
        return sorted(L, key=lambda x: x[1])

    def bench_generator(self):
        L = ((k, v) for (k, v) in self.d.items())
        return sorted(L, key=lambda x: x[1])

    def bench_lambda(self):
        return sorted(self.d.items(), key=lambda x: x[1])

    def bench_formalFnInner(self):
        def fninner(x):
            return x[1]
        return sorted(self.d.items(), key=fninner)

    def bench_formalFnOuter(self):
        return sorted(self.d.items(), key=fnouter)


class SortLargerDictByValue(SortDictByValue):
    '''Sort Dict with 1000 Keys by Value'''
    times = 1000

    def before_class(self):
        self.d = dict(zip(range(1000), range(1000)))
