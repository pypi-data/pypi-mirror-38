import getpass
import logging
import sys

from prvsnlib.utils.ssh import Ssh

class Remote:

    def __init__(self,
                 hostname='localhost',
                 username=getpass.getuser(),
                 no_copy_keys=False,
                 package='package.pyz',
                 sudo=True):
        self._hostname = hostname
        self._username = username
        self._no_copy_keys = no_copy_keys
        self._package = package
        self._sudo = sudo

    def manage_public_keys(self, ssh):
        if not self._no_copy_keys:
            logging.header('Copying public keys to ' + self._hostname)
            ssh.copy_public_keys()

            all_lines = []
            for line in ssh.output:
                logging.debug(line)
                all_lines.append(line)

            if 'skipped because they already exist' in ''.join(all_lines):
                logging.success('Public keys already present. Skipping.')
            else:
                if ssh.returncode is None:
                    pass
                elif ssh.returncode == 0:
                    logging.success('Public keys copied.')
                elif ssh.returncode > 0:
                    logging.error('Could not copy public key')


    def copy_package(self, ssh):
        logging.header('Sending package to ' + ssh.hostname)
        ssh.copy_to(self._package, self._package)

        for line in ssh.output:
            logging.debug(line)

        exit_code = 0

        if ssh.error:
            for line in ssh.error:
                logging.error(line)
                exit_code = 1

        if ssh.returncode is None:
            pass
        elif ssh.returncode == 0:
            logging.debug('return code: 0')
        elif ssh.returncode > 0:
            logging.error('return code: ' + str(ssh.returncode))
            exit_code = 1

        if exit_code:
            logging.error('Sending package failed.')
            sys.exit(exit_code)

        logging.success('Sent.')

    def execute_package(self, ssh):
        logging.header('Remotely executing package on ' + ssh.hostname)

        ssh.run_command(['python', self._package], sudo=self._sudo)

        if ssh.output:
            for line in ssh.output:
                logging.info(line)

        exit_code = 0

        if ssh.error:
            for line in ssh.error:
                logging.error(line)
                exit_code = 1

        if ssh.returncode is None:
            pass
        elif ssh.returncode == 0:
            logging.debug('return code: 0')
        elif ssh.returncode > 0:
            logging.error('return code: ' + str(ssh.returncode))
            exit_code = 1

        if exit_code:
            logging.error('Remotely executing package failed.')
            sys.exit(exit_code)

        logging.success('Remote package executed.')

    def run(self):

        ssh = Ssh(hostname=self._hostname, username=self._username)

        self.manage_public_keys(ssh)
        self.copy_package(ssh)
        self.execute_package(ssh)

        logging.success('Remote provisioned.')