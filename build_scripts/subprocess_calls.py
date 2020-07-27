"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
build script to make sub process calls"""

import subprocess
import sys
import os


def call_subprocess(cmd):
    """
    Function to call subprocess to issue system commands

    Parameters:
      cmd (string): command to be executed at system level.

    Returns:
    sub-process return value.
    """
    working_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
    retval = subprocess.call(cmd, shell=True, cwd=working_dir)
    if retval != 0:
        print("Error occurred while processing %s:" % cmd)
        sys.exit(1)
    return retval
