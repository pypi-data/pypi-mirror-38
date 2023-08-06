import subprocess

from prvsnlib.utils.run import run
from ..task import Task


class PackageAction:
    UPDATE = 'update'
    UPGRADE = 'upgrade'
    INSTALL = 'install'
    REMOVE = 'remove'

class PackageTask(Task):

    _packageClass = False

    @classmethod
    def package(cls, *args, **kwargs):
        if not cls._packageClass:
            if subprocess.check_output(['which', 'brew']):
                cls._packageClass = HomebrewPackageTask
            elif subprocess.check_output(['which', 'apt-get']):
                cls._packageClass = AptPackageTask
            elif subprocess.check_output(['which', 'yum']):
                cls._packageClass = YumPackageTask
        return cls._packageClass(*args, **kwargs)

    def __init__(self, package_name, action, secure):
        Task.__init__(self, secure)
        self._package_name = package_name
        self._action = action

    def __str__(self):
        if self._action == PackageAction.INSTALL:
            return 'Install package "' + self._package_name + '".'
        elif self._action == PackageAction.REMOVE:
            return 'Remove package "' + self._package_name + '".'
        elif self._action == PackageAction.UPDATE:
            return 'Update packages list.'
        elif self._action == PackageAction.UPGRADE:
            return 'Upgrade all packages.'
        return 'Package action "' + str(self._action) + '" not implemented.'

    def run(self):
        return '', 'Not implemented.'


class HomebrewPackageTask(PackageTask):
    def run(self):
        if self._action == PackageAction.UPDATE:
            cmd, out, ret, err = run(['brew', 'update'])
        elif self._action == PackageAction.UPGRADE:
            cmd, out, ret, err = run(['brew', 'upgrade', self._package_name])
        elif self._action == PackageAction.INSTALL:
            cmd, out, ret, err = run(['brew', 'install', self._package_name])
        elif self._action == PackageAction.REMOVE:
            cmd, out, ret, err = run(['brew', 'uninstall', self._package_name])
        if err:
            return cmd, err
        if ret:
            return cmd, out
        return cmd+'\n'+out, ''


class AptPackageTask(PackageTask):
    def run(self):
        if self._action == PackageAction.UPDATE:
            cmd, out, ret, err = run(['apt-get', 'update'])
        elif self._action == PackageAction.UPGRADE:
            cmd, out, ret, err = run(['apt-get', 'upgrade', '-y', '--no-install-recommends'])
        elif self._action == PackageAction.INSTALL:
            cmd, out, ret, err = run(['apt-get', 'install', '-y', '--no-install-recommends', self._package_name])
        elif self._action == PackageAction.REMOVE:
            cmd, out, ret, err = run(['apt-get', 'remove', '-y', self._package_name])
        if err:
            return cmd, err
        if ret:
            return cmd, out
        return cmd+'\n'+out, ''


class YumPackageTask(PackageTask):
    def run(self):
        if self._action == PackageAction.UPDATE:
            cmd, out, ret, err = run(['yum', 'update'])
        elif self._action == PackageAction.UPGRADE:
            cmd, out, ret, err = run(['yum', 'upgrade', '-y'])
        elif self._action == PackageAction.INSTALL:
            cmd, out, ret, err = run(['yum', 'install', '-y', self._package_name])
        elif self._action == PackageAction.REMOVE:
            cmd, out, ret, err = run(['yum', 'remove', '-y', self._package_name])
        if err:
            return cmd, err
        if ret:
            return cmd, out
        return cmd+'\n'+out, ''


def package(d, action=PackageAction.INSTALL, secure=False):
    PackageTask.package(d, action, secure)


def homebrew_package(d, action=PackageAction.INSTALL, secure=False):
    HomebrewPackageTask(d, action, secure)


def apt_package(d, action=PackageAction.INSTALL, secure=False):
    AptPackageTask(d, action, secure)


def yum_package(d, action=PackageAction.INSTALL, secure=False):
    YumPackageTask(d, action, secure)