from minibench import Benchmark

import time


class PauseBenchmark(Benchmark):
    times = 10

    def bench_one_hundredth(self):
        time.sleep(.01)

    def bench_one_tenth(self):
        time.sleep(.1)
