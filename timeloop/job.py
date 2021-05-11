from threading import Thread, Event, Timer
from time import time
import logging
import sys


class Job(Thread):
    def __init__(self, interval, timeout, execute, *args, **kwargs):
        Thread.__init__(self)
        self.stopped = Event()
        self.timeout = timeout
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        logger = logging.getLogger('timeloop-job')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        self.logger = logger
        self.logger.info("Job initialized {}".format(self.execute))

    def out(self):
        self.logger.warning("Timeout in job {}".format(self.execute))
        self.join(0)  # Silently kill the

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)

    # def run(self):
    #     next_period = 0
    #     next_time = time()
    #
    #     while not self.stopped.wait(next_period):
    #         t = Timer(self.timeout.total_seconds(), self.out)
    #         t.start()
    #         self.execute(*self.args, **self.kwargs)
    #         t.cancel()
    #         next_time += self.interval.total_seconds()
    #         next_period = next_time - time()
