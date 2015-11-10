from minibench import Benchmark


class SumBenchmark(Benchmark):
    times = 1000

    def bench_sum(self):
        sum(x for x in range(5))

    def bench_consecutive_add(self):
        total = 0
        for x in range(5):
            total += x
