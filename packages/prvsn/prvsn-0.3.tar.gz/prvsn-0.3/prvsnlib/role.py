import os


class Role:

    def __init__(self, path):
        self._path = path

    def __repr__(self):
        return '<Role ' + self.name + '>'

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return os.path.basename(self._path)

    @property
    def main_file(self):
        return os.path.join(self._path, 'main.py')
