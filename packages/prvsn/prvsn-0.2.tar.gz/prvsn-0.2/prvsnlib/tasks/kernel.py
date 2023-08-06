from prvsnlib.utils.file import add_string_if_not_present_in_file, delete_string_from_file
from ..task import Task
from prvsnlib.utils.run import run


class KernelModuleAction:
    ADD = 'add'
    DEL = 'delete'


class KernelModuleTask(Task):

    def __init__(self, module_name, action, secure):
        Task.__init__(self, secure)
        self._module_name = module_name
        self._action = action

    def __str__(self):
        return str(self._action).capitalize() + ' kernel module "' + self._module_name + '".'

    def checkLoadableModules(self):
        cmd, out, ret, err = run(['which', 'modprobe'])
        if ret or err:
            return 'Cannot find loadable linux modules.'
        return None

    def run(self):
        err = self.checkLoadableModules()
        if err: return '', 'Cannot find loadable linux modules.'

        if self._action == KernelModuleAction.ADD:
            return add_string_if_not_present_in_file('/etc/modules', self._module_name)
        elif self._action == KernelModuleAction.ADD:
            return delete_string_from_file('/etc/modules', self._module_name)

def module(d, action=KernelModuleAction.ADD, secure=False):
    KernelModuleTask(d, action, secure)