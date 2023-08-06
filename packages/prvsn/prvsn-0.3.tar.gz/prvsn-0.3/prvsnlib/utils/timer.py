import datetime
import logging
import time


class Timer:

    def __init__(self):
        self._start = time.time()

    def get(self):
        delta = time.time() - self._start
        logging.info(
            'Elapsed wall time clock: ' + str(delta)
        )
        return self
