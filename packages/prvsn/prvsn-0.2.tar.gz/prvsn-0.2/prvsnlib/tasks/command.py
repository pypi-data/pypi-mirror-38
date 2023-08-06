from prvsnlib.utils.run import run
from ..task import Task


class CommandAction:
    RUN = 'run'


class CommandTask(Task):

    def __init__(self, interpreter, cmd, action, secure):
        Task.__init__(self, secure)
        self._interpreter = interpreter
        self._cmd = cmd
        self._action = action

    def __str__(self):
        return 'Run "' + self._interpreter[0] + '" command'

    def run(self):
        cmd, out, ret, err = run(self._interpreter, input=self._cmd)
        cmd = cmd + '\n'
        if err:
            return cmd, err
        if ret:
            return cmd, out
        return cmd+out, ''


def command(interpreter, cmd, action=CommandAction.RUN, secure=False):
    CommandTask(interpreter, cmd, action, secure)

def bash(cmd, action=CommandAction.RUN, secure=False):
    CommandTask(['bash', '-e'], cmd, action, secure)

def ruby(cmd, action=CommandAction.RUN, secure=False):
    CommandTask(['ruby'], cmd, action, secure)
