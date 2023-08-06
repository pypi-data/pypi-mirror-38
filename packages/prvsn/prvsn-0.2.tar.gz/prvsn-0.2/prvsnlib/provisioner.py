import getpass
import importlib
import logging
import os
import sys

import prvsnlib.log

from prvsnlib.queue import Queue
from prvsnlib.role import Role
from prvsnlib.task import Task


class Provisioner:

    def __init__(self, runbook, roles, queue=Queue(), extra_imports={}, share_locals=False):
        logging.debug('Provisioner init.')

        self._runbook = runbook
        self._roles = roles

        self._queue = queue
        Task.setQueue(queue)
        Task.setRunBook(self._runbook)

        self._extra_imports = extra_imports
        self._share_locals = share_locals
        self._run_locals = {}

    def builtin_imports(self):
        logging.debug('Provisioner builtin imports.')
        return {
            'prvsnlib.tasks.command': [
                'command',
                'bash',
                'ruby',
            ],
            'prvsnlib.tasks.file': [
                'file',
            ],
            'prvsnlib.tasks.kernel': [
                'module',
            ],
            'prvsnlib.tasks.package': [
                'package',
                'homebrew_package',
                'apt_package',
                'yum_package',
            ],
        }

    def add_task(self, task):
        self._queue.append(task)

    def run_locals(self):
        logging.debug('Provisioner creating run locals.')
        if not self._run_locals or not self._share_locals:
            run_locals = {}
            to_import = self.builtin_imports()
            to_import.update(self._extra_imports)
            for module_name, symbols in to_import.items():
                module = importlib.import_module(module_name)
                for symbol in symbols:
                    run_locals[symbol] = getattr(module, symbol)
            self._run_locals = run_locals
        return self._run_locals

    def user_check(self):
        logging.info('Running Provisioner as user "' + getpass.getuser() + '"')
        if getpass.getuser() != 'root':
            logging.warning('Provisioning is not running as root (add --sudo)')

    def run(self):
        self.user_check()

        logging.header('Runbook ' + self._runbook.path)
        self.build_roles()
        self.run_tasks()

    def build_roles(self):
        logging.debug('Provisioner building roles.')
        for role in self._roles:
            role = Role('role', os.path.join(self._runbook.path, 'roles', role))
            Task.setRole(role)

            with open(role.main_file) as f:
                code = compile(f.read(), role.path, 'exec')
                exec(code, self.run_locals())

    def run_tasks(self):
        logging.debug('Provisioner running tasks.')

        if not self._queue.tasks:
            logging.error('No tasks. Nothing to do.')

        for task in self._queue.tasks:
            logging.header(str(task))

            out, err = task.run()
            if task.secure: logging.info('(secure: output omitted)')
            else: logging.info(out)

            if err:
                if not task.secure: logging.error(err)
                logging.error('Task failed.')
                sys.exit(1)
        logging.success('Provisioned.')