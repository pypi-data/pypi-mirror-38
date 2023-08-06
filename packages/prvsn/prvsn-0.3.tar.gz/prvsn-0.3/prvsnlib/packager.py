import logging
import os
import shutil
import tempfile
import textwrap

import prvsnlib
from prvsnlib.utils.file import mkdir_p
from prvsnlib.utils.zip import zipdir


class Packager:

    def __init__(self, runbook, roles=None, tmpdir=None, dest=None, cleanup=True, verbose=False):
        if roles is None:
            roles = []
        self._runbook = runbook
        self._roles = roles
        self._tmpdir = tmpdir
        self._dest = dest
        self._verbose = verbose
        self._cleanup = cleanup

    @property
    def prvsnlib_path(self):
        path = os.path.dirname(prvsnlib.__file__)
        logging.debug('Path to prvsnlib is ' + path)
        return path

    @property
    def package_main_contents(self):
        return textwrap.dedent('''
            #!/usr/bin/python
            
            import logging
            import os
            import tempfile
            import shutil
            import zipfile 
        
            from prvsnlib.provisioner import Provisioner
            from prvsnlib.runbook import Runbook
            
            def extract_runbook():
                d = tempfile.mkdtemp()
                logging.debug('Extracting runbook to ' + d)
                my_archive = os.path.dirname(__file__) 
                zf = zipfile.ZipFile(my_archive)
                zf.extractall(d)
                return d
                
            def delete_runbook(d):
                logging.debug('Cleaning up runbook ' + d)
                shutil.rmtree(d)

            def main():
                logging.root.setLevel(logging.{loglevel})

                d = extract_runbook()
                Provisioner(
                    Runbook(os.path.join(d, 'runbook')),
                    {roles},
                ).run()
                delete_runbook(d)

            if __name__ == "__main__":
                main()
        ''').strip().format(
            roles=self._roles,
            loglevel=('DEBUG' if self._verbose else 'INFO')
        )

    def build_package(self):
        logging.header('Packaging runbook "' + self._runbook.path + '"')

        if not self._dest:
            fd, self._dest = tempfile.mkstemp(suffix='.pyz')

        dest_path = os.path.dirname(self._dest)
        mkdir_p(dest_path)

        self.prepare_package()

        logging.debug('Building package at "' + self._dest + '"')

        zipdir(
            self._tmpdir,
            self._dest,
        )

        self.cleanup_package()

        logging.success('Packaged.')
        return self._dest

    def write_package_main(self, path):
        file = os.path.join(path, '__main__.py')
        logging.debug('Writing package main file at "' + file + '"')

        with open(file, 'w') as f:
            f.write(self.package_main_contents)
        os.chmod(file, 0o550)

    def prepare_package(self):
        if not self._tmpdir:
            self._tmpdir = tempfile.mkdtemp()

        if not os.path.exists(self._tmpdir):
            mkdir_p(self._tmpdir)

        logging.debug('Preparing package at "' + self._tmpdir + '"')

        shutil.copytree(
            self.prvsnlib_path,
            os.path.join(self._tmpdir, 'prvsnlib'),
            ignore=shutil.ignore_patterns('*.pyc', '__pycache__')
        )
        shutil.copytree(
            self._runbook.path,
            os.path.join(self._tmpdir, 'runbook')
        )
        self.write_package_main(self._tmpdir)

    def cleanup_package(self):
        if self._cleanup:
            logging.debug('Cleaning up package temp dir')
            shutil.rmtree(self._tmpdir)
