import logging
import os

from prvsnlib.context import context
from prvsnlib.utils.file import mkdir_p, copy_file
from prvsnlib.utils.file import chown as chown_util


class FileAction:
    ADD = 'add'
    REMOVE = 'remove'


def file(a, b=None,
         replacements={},
         owner=None, group=None,
         diff=True,
         action=FileAction.ADD,
         secure=False):

    if action == FileAction.ADD:
        logging.header('Setting up file ' + b)

        base = os.path.basename(b)
        mkdir_p(base)

        global context

        copy_file(
            a,
            b,
            replacements=replacements,
            relative=os.path.join(context.role.path, 'files'),
            diff=diff
        )

        if owner or group:
            chown_util(b, owner, group, recursive=False)

    elif action == FileAction.REMOVE:
        logging.header('Removing file ' + a)
        os.unlink(a)

    else:
        raise Exception('Invalid action')


def chown(path,
          owner=None, group=None,
          recursive=False):
    logging.header('Changing ownership of file ' + path)
    chown_util(path, owner, group, recursive)