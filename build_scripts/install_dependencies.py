"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
build script to install dependencies"""
import os
from subprocess_calls import call_subprocess


def install_pip():
    """
    Installs the dependent packages
    """
    pip_install_txt = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "build_test_dependencies.txt")
    call_subprocess("python3 -m pip install -r %s" % pip_install_txt)
    print("Stage install dependencies -- COMPLETED --")


if __name__ == "__main__":
    install_pip()
