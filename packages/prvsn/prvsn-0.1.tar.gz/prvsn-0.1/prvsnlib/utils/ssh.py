import getpass

class ssh:
    def __init__(self, remote, user=getpass.getuser()):
        self._remote = remote
        self._user = user

    def __str__(self):
        return '<SSH ' + self._user + '@' + self._remote + '>'

