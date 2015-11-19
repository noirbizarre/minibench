from minibench import Benchmark


class FailBenchmark(Benchmark):

    def bench_failure(self):
        raise Exception('I failed')
