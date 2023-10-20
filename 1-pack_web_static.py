#!/usr/bin/python3
""" this module handles packing up"""
from datetime import datetime
import tarfile
import os
from fabric.api import local


def do_pack():
    """ method handles the packing up file"""
    name = (f"web_static_{datetime.now().year}{datetime.now().month}"
            f"{datetime.now().day}{datetime.now().hour}{datetime.now().minute}"
            f"{datetime.now().second}")
    M_name = f"{name}.tgz"
    F_name = f"versions/{M_name}"

    if not os.path.exists("versions"):
        os.makedirs("versions")

    with tarfile.open(F_name, 'w:gz') as archive:
        archive.add('web_static')

    if os.path.exists(F_name):
        return F_name
    else:
        return None
