import logging
import os
import sys


def validate_runbook(runbook):
    if os.path.isdir(runbook._path):
        return True
    else:
        logging.error('Argument "' + runbook._path + '" is not a valid runbook path.')
        sys.exit(1)

def validate_roles(runbook, roles):
    if not roles:
        logging.error('No roles specified. Nothing to do.')
        sys.exit(1)
    for role in roles.split(','):
        if role not in [r.name for r in runbook.roles]:
            logging.error('Argument "' + role + '" is not a valid role in runbook.')
            sys.exit(1)
    return True