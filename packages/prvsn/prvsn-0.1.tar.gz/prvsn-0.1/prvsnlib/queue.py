
class Queue:

    def __init__(self):
        self._queue = []

    def __len__(self):
        return len(self._queue)

    def append(self, task):
        self._queue.append(task)

    @property
    def tasks(self):
        return self._queue