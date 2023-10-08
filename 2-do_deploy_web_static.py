#!/usr/bin/python3
""" This script handles packing up and distributing the web_static code"""

import os
from fabric import Connection, task
from datetime import datetime
import tarfile

# Define the remote hosts
env_hosts = ['52.86.222.148', '3.85.41.223']

@task
def do_deploy(archive_path):
    """Distribute the archive to the web servers and set up the deployment"""
    if not os.path.exists(archive_path):
        print("Archive not found.")
        return False

    try:
        # Extract the filename without extension
        file_name = os.path.basename(archive_path)
        name, _ = os.path.splitext(file_name)

        for host in env_hosts:
            # Upload the archive to the /tmp/ directory of each web server
            with Connection(host) as conn:
                conn.put(archive_path, '/tmp/')

                # Uncompress the archive to the folder on each web server
                conn.run(f'mkdir -p /data/web_static/releases/{name}/')
                conn.run(f'tar -xzf /tmp/{file_name} -C /data/web_static/releases/{name}/')

                # Delete the archive from each web server
                conn.run(f'rm /tmp/{file_name}')

                conn.run(f'mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/')
                conn.run(f'rm -rf /data/web_static/releases/{name}/web_static')

                # Delete the symbolic link /data/web_static/current from each web server
                conn.run('rm -rf /data/web_static/current')

                # Create a new symbolic link on each web server
                conn.run(f'ln -s /data/web_static/releases/{name}/ /data/web_static/current')

        print('New version deployed')
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False  

