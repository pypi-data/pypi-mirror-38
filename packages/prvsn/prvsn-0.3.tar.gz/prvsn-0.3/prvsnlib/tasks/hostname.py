import logging

from prvsnlib.utils.run import Run

def hostname(name, secure=False):
    logging.header('Hostname ' + name)
    Run(['hostnamectl', 'set-hostname', name]).run()
