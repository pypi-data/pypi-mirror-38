"""Setuptools post install script."""

import errno
import getpass
import os
import shutil
import sys


def run(install):
    """Runs all post install hooks."""
    _copy_zsh_ext(install)


def _copy_zsh_ext(install):
    """Copy zsh extension to funky config directory."""
    this_dir = os.path.dirname(os.path.realpath(__file__))
    root = install.root if install.root else ''

    if 'XDG_DATA_HOME' in os.environ:
        xdg_data_dir = root + os.environ['XDG_DATA_HOME']
    else:
        home = 'Users' if sys.platform == 'darwin' else 'home'
        user = getpass.getuser()

        if user == 'root':
            xdg_data_dir = root + "/usr/share/funky"
        else:
            xdg_data_dir = root + "/{}/{}/.local/share/funky".format(home, user)

    _create_dir(xdg_data_dir)

    src = '{}/zsh/funky.zsh'.format(this_dir)
    dest = '{}/funky.zsh'.format(xdg_data_dir)

    shutil.copyfile(src, dest)


def _create_dir(directory):
    """Create directory."""
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            return


if __name__ == "__main__":
    run()
