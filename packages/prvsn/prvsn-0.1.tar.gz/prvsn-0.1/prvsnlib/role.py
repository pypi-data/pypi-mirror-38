import os

class Role:

    def __init__(self, name, path):
        self._name = name
        self._path = path

    def __repr__(self):
        return '<Role "' + self._name + '" (' + self._path + ')>'

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def main_file(self):
        return os.path.join(self._path, 'main.py')