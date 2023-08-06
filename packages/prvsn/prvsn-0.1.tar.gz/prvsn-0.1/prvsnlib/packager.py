import logging
import os
import shutil
import tempfile
import textwrap
import zipapp

import prvsnlib
from prvsnlib.utils.file import mkdir_p


class Packager:

    def __init__(self, runbook, roles=[], tmpdir=None, dest=None, cleanup=True, verbose=False):
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
            import zipfile 
        
            from prvsnlib.provisioner import Provisioner
            from prvsnlib.runbook import Runbook
            
            def extract_runbook():
                my_archive = os.path.dirname(__file__) 
                zf = zipfile.ZipFile(my_archive)
                dir = tempfile.mkdtemp()
                zf.extractall(dir)
                return dir

            def main():
                logging.root.setLevel(logging.{loglevel})

                dir = extract_runbook()
                Provisioner(
                    Runbook('runbook', os.path.join(dir, 'runbook')),
                    {roles},
                ).run()

            if __name__ == "__main__":
                main()
        ''').strip().format(
            roles=self._roles,
            loglevel=('DEBUG' if self._verbose else 'INFO')
        )

    def build_package(self):
        logging.header('Packaging runbook "' + self._runbook._path + '"')

        if not self._dest:
            self._dest = tempfile.mkstemp(suffix='.pyz')

        dest_path = os.path.dirname(self._dest)
        if not os.path.exists(dest_path):
            mkdir_p(dest_path)

        self.prepare_package()

        logging.info('Building package at "' + self._dest + '"')
        zipapp.create_archive(
            self._tmpdir,
            target=self._dest
        )
        self.cleanup_package()
        logging.success('Packaged.')

    def write_package_main(self, path):
        file = os.path.join(path, '__main__.py')
        logging.info('Writing package main file at "' + file + '"')

        with open(file, 'w') as f:
            f.write(self.package_main_contents)
        os.chmod(file, 0o550)

    def prepare_package(self):
        if not self._tmpdir:
            self._tmpdir = tempfile.mkdtemp()

        if not os.path.exists(self._tmpdir):
            mkdir_p(self._tmpdir)

        logging.info('Preparing package at "' + self._tmpdir + '"')

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
            logging.info('Cleaning up package temp dir')
            shutil.rmtree(self._tmpdir)