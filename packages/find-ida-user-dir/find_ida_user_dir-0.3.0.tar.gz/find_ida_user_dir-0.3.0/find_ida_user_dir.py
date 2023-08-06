'''
Created on 14 Sep 2018

@author: Mike Thomas
'''
import os
import click

_VERSION = "0.3.0"


def _find_windows():
    path = os.getenv("APPDATA")
    if path:
        return os.path.join(path, 'Hex-Rays', 'IDA Pro')
    return ""


def _find_starnix():
    path = os.path.expanduser("~")
    if path:
        return os.path.join(path, '.idapro')


def find_path(subdir=None):
    """Find the IDA user directory for the current user on the current platform.

    Returns the path to the IDA user directory. No guarantee is made of the
    existence of the directory, but it is the correct path as defined by the
    IDA documentation.

    If subdir is given then the path to that subdirectory of the IDA user
    directory is returned.
    """
    path = None
    try:
        import ida_diskio
        path = ida_diskio.get_user_idadir()
    except ImportError:
        path = os.getenv("IDAUSR")
        if path:
            path = path.split(os.path.pathsep)[0]
        elif os.name == "nt":
            path = _find_windows()
        else:
            path = _find_starnix()
    if path and subdir:
        path = os.path.join(path, subdir)
    return path


@click.command()
@click.version_option(_VERSION)
@click.argument("subdir",
                default="")
def _main(subdir=""):
    """Find the IDA user directory for the current user on the current platform.

    Returns the path to the IDA user directory. No guarantee is made of the
    existence of the directory, but it is the correct path as defined by the
    IDA documentation.

    If subdir is given then the path to that subdirectory of the IDA user
    directory is returned.
    """
    click.echo(find_path(subdir))


if __name__ == '__main__':
    _main()
