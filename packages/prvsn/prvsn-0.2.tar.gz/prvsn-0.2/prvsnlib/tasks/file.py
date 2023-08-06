import os

from prvsnlib.utils.file import mkdir_p, get_replace_write_file
from prvsnlib.utils.string import replace_all
from ..task import Task


class FileAction:
    ADD = 'add'


class FileTask(Task):

    def __init__(self, source, file, replacements, action, secure):
        Task.__init__(self, secure)
        self._source = source
        self._file = file
        self._action = action
        self._replacements = replacements

    def __str__(self):
        return 'Setting up file "' + self._file + '"'

    def run(self):
        mkdir_p(os.path.dirname(self._file))
        return get_replace_write_file(self._source,
                                      os.path.join(self._role.path, 'files'),
                                      self._replacements,
                                      self._file)


def file(source, file, replacements={}, action=FileAction.ADD, secure=False):
    FileTask(source, file, replacements, action, secure)