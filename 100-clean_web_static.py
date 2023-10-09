#!/usr/bin/python3
"""Fabric script to clean up old archives"""

from fabric.api import *
import os


env.hosts = ['52.86.222.148', '3.85.41.223']


def do_clean(number=0):
    """
    Delete old archives from versions and releases folders
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]