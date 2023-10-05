#!/usr/bin/python3
"""This module handles packing up, distribution, and clean up"""

import os
from fabric.api import local, put, env, run

env.hosts = ['xx-web-01', 'xx-web-02']


def do_clean(number=0):
    """A method that cleans up out-of-date archives"""
    number = int(number)

    # keep at least one version if number <= 1
    if number <= 1:
        number = 2
    else:
        number += 1

    # Delete all unnecessary archives in the versions folder
    local(
        'ls -1t versions | tail -n +{} | xargs -I {} rm -- versions/{}'.format(
            number, '{}'))

    # Delete all unnecessary archives in the /data/web_static/releases
    # folder of both web servers
    run('ls -1t /data/web_static/releases | tail -n +{} | xargs -I {} rm -rf -- /data/web_static/releases/{}'.format(
        number, '{}'))


if __name__ == "__main__":
    do_clean()
