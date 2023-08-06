import getpass
import itertools
import logging
import subprocess


STDIN_FILENO = 0
STDOUT_FILENO = 1
STDERR_FILENO = 2

CHILD = 0


class Run():

    def __init__(self, commands, stdin=None, user=None):

        self._commands = commands
        self._stdin_data = stdin
        self._user = user

        self._process = None
        self._output_generator = None


    def run(self):
        logging.debug('Popen.')

        user_cmd = []
        if self._user and self._user != getpass.getuser():
            user_cmd = ['sudo', '-u', self._user]

        self._process = subprocess.Popen(
            user_cmd + self._commands,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            bufsize=0, universal_newlines=True)

        if self._stdin_data:
            logging.debug('Writing to stdin.')
            self._process.stdin.write(self._stdin_data)
            self._process.stdin.close()

        logging.debug('Process output')

        def output_generator():
            for line in iter(self._process.stdout.readline, b''):

                if line == '' and not self._process.poll() is None:
                    break

                if line != '':
                    yield line.strip()

        self._output_generator, output = itertools.tee(output_generator())

        for line in output:
            logging.info(line)

        logging.debug('Process output done.')

        returncode = self._process.poll()
        if returncode != None and returncode != 0:
            logging.debug('Return code != 0. Raising exception.')
            raise subprocess.CalledProcessError(
                cmd=[_ for _ in self.commands],
                returncode=self._process.returncode,
            )

        return self

    @property
    def commands(self):
        if self._stdin_data:
            for line in self._stdin_data.splitlines():
                if line:
                    yield '(' + ' '.join(self._commands) + ') ' + line
        else:
            yield ' '.join(self._commands)

    @property
    def output(self):
        return self._output_generator