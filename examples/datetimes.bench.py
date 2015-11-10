from minibench import Benchmark

import time
import datetime


class TimeTests(Benchmark):
    '''datetime vs. time'''
    times = 100

    def bench_utcnow(self):
        return datetime.datetime.utcnow().isoformat()[:-6] + '000Z'

    def bench_gmtime(self):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
