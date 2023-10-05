#!/usr/bin/python3
"""This module handles packing up and distribution"""

import os
from fabric.api import local, put, env, run

env.hosts = ['52.86.222.148', '3.85.41.223']


def do_deploy(archive_path):
    """A method that distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the filename without extension
        file_name = os.path.basename(archive_path)
        name, ext = os.path.splitext(file_name)

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension> on
        # the web server
        run(f'mkdir -p /data/web_static/releases/{name}/')
        run(f'tar -xzf /tmp/{file_name} -C /data/web_static/releases/{name}/')

        # Delete the archive from the web server
        run(f'rm /tmp/{file_name}')

        run(f' mv /data/web_static/releases/{name}'
            f'/web_static/* '
            f'/data/web_static/releases/{name}/')

        run(f'rm -rf /data/web_static/releases/{name}/web_static')

        # Delete the symbolic link /data/web_static/current from the web
        # server
        run('rm -rf /data/web_static/current')

        # Create a new the symbolic link /data/web_static/current on the
        # web server, linked to the new version of your code (
        # /data/web_static/releases/<archive filename without extension>)
        run(f'ln -s /data/web_static/releases/{name}/ /data/web_static'
            f'/current')

        return True
    except Exception as e:
        june = str(e)
        return False