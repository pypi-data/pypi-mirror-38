import getpass
import logging
import subprocess

from prvsnlib.utils.run import Run


class PackageAction:
    UPDATE = 'update'
    UPGRADE = 'upgrade'
    INSTALL = 'install'
    REMOVE = 'remove'


class PackageTask:

    _packageClass = None

    @classmethod
    def package(cls, *args, **kwargs):
        if not cls._packageClass:
            try:
                if subprocess.check_output(['which', 'brew']):
                    cls._packageClass = HomebrewPackageTask
            except Exception:
                pass
            try:
                if subprocess.check_output(['which', 'apt-get']):
                    cls._packageClass = AptPackageTask
            except Exception:
                pass
            try:
                if subprocess.check_output(['which', 'yum']):
                    cls._packageClass = YumPackageTask
            except Exception:
                pass
        return cls._packageClass(*args, **kwargs)

    def __init__(self, name='', user=None, action=PackageAction.INSTALL):
        self._name = name.split()
        self._user = user
        self._action = action

    @property
    def header(self):
        if self._action == PackageAction.INSTALL:
            return 'Install package'
        elif self._action == PackageAction.REMOVE:
            return 'Remove package'
        elif self._action == PackageAction.UPDATE:
            return 'Update packages list'
        elif self._action == PackageAction.UPGRADE:
            return 'Upgrade all packages'
        raise Exception('Imvalid action')

    def run(self):
        logging.header(self.header)


class HomebrewPackageTask(PackageTask):
    def run(self):
        super(HomebrewPackageTask, self).run()

        if self._action == PackageAction.UPDATE:
            return Run(['brew', 'update'], user=self._user).run()
        elif self._action == PackageAction.UPGRADE:
            return Run(['brew', 'upgrade'] + self._name, user=self._user).run()
        elif self._action == PackageAction.INSTALL:
            return Run(['brew', 'install'] + self._name, user=self._user).run()
        elif self._action == PackageAction.REMOVE:
            return Run(['brew', 'uninstall'] + self._name, user=self._user).run()


class CaskPackageTask(PackageTask):
    def run(self):
        super(CaskPackageTask, self).run()

        if self._action == PackageAction.UPDATE:
            logging.info('No update function for Cask. Ignoring.')
        elif self._action == PackageAction.UPGRADE:
            return Run(['brew', 'cask', 'upgrade'] + self._name, user=self._user).run()
        elif self._action == PackageAction.INSTALL:
           return Run(['brew', 'cask', 'install'] + self._name, user=self._user).run()
        elif self._action == PackageAction.REMOVE:
            return Run(['brew', 'cask', 'uninstall'] + self._name, user=self._user).run()


class MasPackageTask(PackageTask):
    def run(self):
        super(MasPackageTask, self).run()

        if self._action == PackageAction.UPDATE:
            logging.info('No update function for app store. Ignoring.')
        elif self._action == PackageAction.UPGRADE:
            return Run(['mas', 'upgrade'] + self._name, user=self._user).run()
        elif self._action == PackageAction.INSTALL:
            return Run(['mas', 'install'] + self._name, user=self._user).run()
        elif self._action == PackageAction.REMOVE:
            raise Exception('No remove function for app store.')


class AptPackageTask(PackageTask):
    def run(self):
        super(AptPackageTask, self).run()

        if self._action == PackageAction.UPDATE:
            return Run(['apt-get', 'update']).run()
        elif self._action == PackageAction.UPGRADE:
            return Run(['apt-get', 'upgrade', '-y', '--no-install-recommends'] + self._name).run()
        elif self._action == PackageAction.INSTALL:
            return Run(['apt-get', 'install', '-y', '--no-install-recommends'] + self._name).run()
        elif self._action == PackageAction.REMOVE:
            return Run(['apt-get', 'remove', '-y'] + self._name).run()


class YumPackageTask(PackageTask):
    def run(self):
        super(YumPackageTask, self).run()

        if self._action == PackageAction.UPDATE:
            return Run(['yum', 'update']).run()
        elif self._action == PackageAction.UPGRADE:
            return Run(['yum', 'upgrade', '-y'] + self._name).run()
        elif self._action == PackageAction.INSTALL:
            return Run(['yum', 'install', '-y'] + self._name).run()
        elif self._action == PackageAction.REMOVE:
            return Run(['yum', 'remove', '-y'] + self._name).run()


def package(*args, **kwargs):
    PackageTask.package(*args, **kwargs).run()


def mac_app_store(*args, **kwargs):
    MasPackageTask(*args, **kwargs).run()


def homebrew_package(*args, **kwargs):
    HomebrewPackageTask(*args, **kwargs).run()


def cask_package(*args, **kwargs):
    CaskPackageTask(*args, **kwargs).run()


def apt_package(*args, **kwargs):
    AptPackageTask(*args, **kwargs).run()


def yum_package(*args, **kwargs):
    YumPackageTask(*args, **kwargs).run()
