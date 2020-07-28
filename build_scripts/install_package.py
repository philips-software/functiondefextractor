"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
file used for installing the package"""
import os
import sys
import subprocess


def find_installer():
    """ Function finds the installer full name based on the substring"""
    proj_dist = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))), "dist")
    installer_list = os.listdir(proj_dist)
    return [item for item in installer_list if "functiondefextractor" in item]


def install(package):
    """ Function used for installing the package using the pip installer"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def cmd_package():
    """ Function validates only one installer is present then issues install command"""
    whl_list = [whl for whl in find_installer() if "whl" in whl]
    if len(whl_list) != 1:
        print("unable to find the installer, only one whl file presence is supported!")
        sys.exit(1)
    whl_matching = ''.join(whl_list)
    proj_dist = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))), "dist", whl_matching)
    install(proj_dist)


if __name__ == "__main__":
    cmd_package()
