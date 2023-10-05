#!/usr/bin/python3
"""Fabric script to clean up old archives"""

from fabric.api import env, local, run
from datetime import datetime
import os

from fabric.context_managers import settings

env.hosts = ['52.86.222.148', '3.85.41.223']


def do_clean(number=0):
    """
    Delete old archives from versions and releases folders
    """
    try:
        number = int(number)
        if number < 1:
            number = 1

        # Get the list of archives in versions folder
        local_archives = local("ls -t versions", capture=True).split("\n")
        if number < len(local_archives):
            archives_to_delete = local_archives[number:]
            for archive in archives_to_delete:
                local("rm versions/{}".format(archive))

        # Get the list of archives in releases folder on each server
        for host in env.hosts:
            with settings(host_string=host):
                server_archives = run("ls -t /data/web_static/releases").split("\n")
                if number < len(server_archives):
                    archives_to_delete = server_archives[number:]
                    for archive in archives_to_delete:
                        run("rm -rf /data/web_static/releases/{}".format(archive))
    except ValueError:
        print("Please provide a valid number for the archives to keep.")


if __name__ == "__main__":
    # Change the number to specify how many versions to keep (e.g.,
    # 2 to keep two most recent)
    do_clean(number=0)
