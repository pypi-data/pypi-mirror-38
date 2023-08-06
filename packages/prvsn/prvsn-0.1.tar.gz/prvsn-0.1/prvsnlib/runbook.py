import logging
import os
import textwrap

from .role import Role
from .utils.file import mkdir_p


class Runbook:

    def __init__(self, name, path):
        self._name = name
        self._path = path
        self._roles = []

    def __repr__(self):
        return '<Runbook "' + self._name + '" (' + self._path + ')>'

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def metadata_file(self):
        return os.path.join(self._path, 'metadata.py')

    @property
    def roles(self):
        if not self._roles:
            roles = []
            roles_path = os.path.join(self._path, 'roles')
            if os.path.exists(roles_path):
                for file in os.listdir(roles_path):
                    file_path = os.path.join(self._path, 'roles', file)
                    if os.path.isdir(file_path):
                        main_path = os.path.join(file_path, 'main.py')
                        if os.path.isfile(main_path):
                            role = Role(file, file_path)
                            roles.append(role)
            self._roles = roles

        return self._roles

    def create_scaffolding(self):

        logging.info('Initializing runbook "' + self._path + '"')

        roles_path = os.path.join(self._path, 'roles')
        mkdir_p(roles_path)

        base_roles_path = os.path.join(roles_path, 'base')
        mkdir_p(base_roles_path)

        main_base_roles_path = os.path.join(base_roles_path, 'main.py')
        with open(main_base_roles_path, 'w') as f:
            data = textwrap.dedent('''
                # This is a template for a role

                bash('echo "hello"')

                package('pkill')

                file(
                    'yo.conf', 
                    '/etc/yo.conf', 
                    replacements={
                        'USERNAME': 'arnaud'
                    },
                )
            ''').strip()
            f.write(data)

        files_base_roles_path = os.path.join(base_roles_path, 'files')
        mkdir_p(files_base_roles_path)

        with open(os.path.join(files_base_roles_path, 'yo.conf'), 'w') as f:
            data = textwrap.dedent('''
                username = USERNAME
                dob = 01/01/1970
            ''')
            f.write(data)