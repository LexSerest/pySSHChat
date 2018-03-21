import subprocess

ver = int(subprocess.check_output(['git', 'rev-list', '--all', '--count']))


def get_version():
    return '1.0.%s' % ver
