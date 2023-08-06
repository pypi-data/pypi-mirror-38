import getpass
import logging
import pty
import os

# from prvsnlib.utils.run import run
from prvsnlib.utils.file import mkdir_p

CHILD = 0



class Ssh:

    def __init__(self, hostname='localhost', username=getpass.getuser(), password=None):
        self.hostname = hostname
        self.username = username
        self._password = password

        self._commands = None
        self._pid = None
        self._child_fd = None
        self._returncode = None
        self._exception = None
        self._error = None

    def __str__(self):
        return '<SSH ' + self.username + '@' + self.hostname + '>'

    @property
    def ssh_config_dir(self):
        home = os.path.expanduser("~")
        return os.path.join(home, '.ssh')

    @property
    def key_file(self):
        return os.path.join(self.ssh_config_dir, 'id_rsa')

    @property
    def public_key_file(self):
        return self.key_file + '.pub'

    def create_public_key_file_if_not_exist(self, key_file=None):
        if not key_file:
            key_file = self.key_file
        public_key_file = key_file + '.pub'
        if not os.path.exists(public_key_file):
            config_dir = os.path.dirname(key_file)
            mkdir_p(config_dir)
            os.chmod(config_dir, 0o700)
            logging.info('No public key found; creating a new key at "' + self.public_key_file + '"')
            self.run([
                'ssh-keygen',
                '-t', 'rsa',
                '-b', '4096',
                '-f', key_file,
                '-N', ''
            ])

    def copy_public_keys(self):
        self.create_public_key_file_if_not_exist()

        return self.run([
            '/usr/bin/ssh-copy-id',
            self.username + '@' + self.hostname,
        ])

    def run_command(self, commands, sudo=False):
        commands_to_run = [
            '/usr/bin/ssh',
            '-t',
            self.username + '@' + self.hostname,
        ]

        if sudo:
            commands_to_run += ['sudo', '-p "sudo password: "']

        commands_to_run += commands

        return self.run(commands_to_run)

    def copy_to(self, src, dest):

        if os.path.dirname(dest):
            self.run_command('mkdir -p ' + os.path.dirname(dest))

        return self.run([
            '/usr/bin/scp',
            src,
            self.username + '@' + self.hostname + ':' + dest,
        ])

    def copy_from(self, src, dest):
        mkdir_p(os.path.dirname(dest))
        return self.run([
            '/usr/bin/scp',
            self.username + '@' + self.hostname + ':' + src,
            dest,
        ])

    def run(self, commands):
        logging.debug('Running "' + ' '.join(commands) + '"')

        pid, child_fd = pty.fork()

        if pid == CHILD:
            os.execv(commands[0], commands)

        self._commands = commands
        self._pid = pid
        self._child_fd = child_fd
        self._returncode = None
        self._exception = None
        self._error = None

        return self


    @property
    def command(self):
        return ' '.join(self._commands)

    @property
    def output(self):

        password = ''
        password_attempted = False

        while True:
            try:
                r = os.read(self._child_fd, 1024).strip()
                wpid, wret, wres = os.wait4(self._pid, os.WNOHANG)
                if wpid:
                    self._returncode = wret
            except Exception as e:
                break
            lower = r.lower()

            if b'are you sure you want to continue connecting' in lower:
                logging.debug('Adding host to known hosts')
                os.write(self._child_fd, b'yes\n')

            elif b'sudo password:' in lower:
                password = getpass.getpass(prompt='Password for sudo: ')

                logging.debug('Sending sudo password')
                os.write(self._child_fd, password.encode('utf-8') + b'\n')

            elif b'password:' in lower:
                if self._password:
                    password = self._password
                else:
                    password = getpass.getpass(prompt='Password for user "' + self.username + '": ')
                    password_attempted = True

                logging.debug('Sending SSH password')
                os.write(self._child_fd, password.encode('utf-8') + b'\n')

            elif r:
                yield r.decode('utf-8')

            if wret:
                self._error = ['return code: ' + str(wret)]
                break

            if password_attempted and password and lower and b'uthentication fail' not in lower:
                logging.debug('SSH authenticated')
                self._password = password
                password_attempted = False

    @property
    def returncode(self):
        try:
            pid, ret = os.wait()
            return ret
        except:
            if self._returncode is None:
                return len(self._error)
            return self._returncode

    @property
    def error(self):
        try:
            pid, ret = os.wait()
            if pid:
                self._returncode = ret
        except:
            pass
        if self._exception:
            return str(self._exception)
        return self._error