import logging
import os
import zipfile

from prvsnlib.context import context
from prvsnlib.utils.file import mkdir_p, chown


class ZipAction:
    EXTRACT = 'extract'


def unzip(src, dest, owner=None, group=None, action=ZipAction.EXTRACT):
    if action == ZipAction.EXTRACT:
        logging.header('Extract zip file '+ src)

        mkdir_p(os.path.dirname(dest))

        global context

        if not os.path.exists(src):
            source = os.path.join(context.role.path, 'files', src)

        zf = zipfile.ZipFile(src)
        r = zf.extractall(dest)

        if owner or group:
            chown(dest, owner, group, recursive=True)
    else:
        raise Exception('Invalid action')





