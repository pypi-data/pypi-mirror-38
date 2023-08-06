from .queue import Queue


class Task:

    _queue = None
    _runbook = None
    _role = None

    @classmethod
    def setQueue(cls, queue):
        cls._queue = queue

    @classmethod
    def setRunBook(cls, runbook):
        cls._runbook = runbook

    @classmethod
    def setRole(cls, role):
        cls._role = role

    @property
    def secure(self):
        return self._secure

    def __init__(self, secure=False):
        self.__class__._queue.append(self)
        self._runbook = self.__class__._runbook
        self._role = self.__class__._role
        self._secure = secure

    def run(self):
        out = 'No output'
        err = 'Task run not implemented'
        return out, err
