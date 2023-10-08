#!/usr/bin/python3
"""This script handles packing up and distributing the web_static code"""

import os
from fabric import Connection, task
from datetime import datetime
import tarfile

# Define the remote hosts
env_hosts = ['52.86.222.148', '3.85.41.223']

@task
def do_pack():
    """Create a compressed archive of the web_static folder"""
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    archive_name = f"web_static_{timestamp}.tgz"

    if not os.path.exists("versions"):
        os.makedirs("versions")

    with tarfile.open(f"versions/{archive_name}", 'w:gz') as archive:
        archive.add('web_static', arcname=os.path.basename('web_static'))

    archive_path = os.path.join(os.getcwd(), "versions", archive_name)
    if os.path.exists(archive_path):
        return archive_path
    else:
        return None

@task
def do_deploy(archive_path):
    """Distribute the archive to the web servers and set up the deployment"""
    if not os.path.exists(archive_path):
        print("Archive not found.")
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        with Connection(env_hosts[0]) as conn:
            conn.put(archive_path, '/tmp/')

            # Extract the filename without extension
            file_name = os.path.basename(archive_path)
            name, _ = os.path.splitext(file_name)

            # Uncompress the archive to the folder
            conn.run(f'mkdir -p /data/web_static/releases/{name}/')
            conn.run(f'tar -xzf /tmp/{file_name} -C /data/web_static/releases/{name}/')

            # Delete the archive from the web server
            conn.run(f'rm /tmp/{file_name}')

            conn.run(f'mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/')
            conn.run(f'rm -rf /data/web_static/releases/{name}/web_static')

            # Delete the symbolic link /data/web_static/current from the web server
            conn.run('rm -rf /data/web_static/current')

            # Create a new symbolic link
            conn.run(f'ln -s /data/web_static/releases/{name}/ /data/web_static/current')

        print('New version deployed!')
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
