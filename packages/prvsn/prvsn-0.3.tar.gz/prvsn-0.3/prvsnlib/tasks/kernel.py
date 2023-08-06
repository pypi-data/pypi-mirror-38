import logging

from prvsnlib.utils.file import add_string_if_not_present_in_file, delete_string_from_file


class KernelModuleAction:
    ADD = 'add'
    REMOVE = 'remove'


def module(module, action=KernelModuleAction.ADD, secure=False):
    if action == KernelModuleAction.ADD:
        logging.header('Add kernel module' + module)
        add_string_if_not_present_in_file('/etc/modules', module)

    elif action == KernelModuleAction.REMOVE:
        logging.header('Remove kernel module' + module)
        delete_string_from_file('/etc/modules', module)

    else:
        raise Exception('Invalid action')
