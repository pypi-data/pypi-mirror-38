import getpass
import importlib
import logging
import os
import subprocess
import sys

from prvsnlib.log import StdoutLogger
from prvsnlib.role import Role
from .context import context


class Provisioner:

    def __init__(self, runbook, roles, extra_imports={}):
        logging.debug('Provisioner init')

        self._runbook = runbook
        self._roles = roles

        self._extra_imports = extra_imports
        self._run_locals = {}

    def run(self):
        logging.debug('Provisioner run')

        def user_check():
            logging.info('Running provisioner as user ' + getpass.getuser())
            if getpass.getuser() != 'root':
                logging.warning('Provisioning not running as root (use --sudo if needed)')

        user_check()

        logging.header('Runbook ' + self._runbook.path)
        logging.header('Roles ' + ', '.join(self._roles))

        def exec_locals(runbook, role):

            to_import = {'prvsnlib.tasks': ['*']}
            to_import.update(self._extra_imports)

            exec_locals = {}
            for module_name, symbol_names in to_import.items():
                module = importlib.import_module(module_name)
                for symbol_name in symbol_names:
                    if symbol_name == '*':
                        exec_locals.update(module.__dict__)
                    else:
                        exec_locals[symbol_name] = getattr(module, symbol_name)
            exec_locals['runbook'] = runbook
            exec_locals['role'] = role
            return exec_locals

        try:
            with StdoutLogger():
                for role in self._roles:
                    role = Role(os.path.join(self._runbook.path, 'roles', role))

                    global provisioning_context

                    context.runbook = self._runbook
                    context.role = role

                    with open(role.main_file) as f:
                        code = compile(f.read(), role.path, 'exec')
                    exec(code, exec_locals(self._runbook, role))

        except subprocess.CalledProcessError as e:
            logging.error(str(e))
            logging.error('return code: ' + str(e.returncode))
            sys.exit(1)

        logging.success('Provisioned.')