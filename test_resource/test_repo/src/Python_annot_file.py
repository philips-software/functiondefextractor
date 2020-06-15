from __future__ import print_function

import csv
import sys
import subprocess
import shutil
import os

def create_parser(args):
    """ Function which add the command line arguments required for the commandline input
    of guardrails"""
    # Create the parser
    func_parser = argparse.ArgumentParser(description='Guardrails for python programs')

    # Add the arguments
    func_parser.add_argument('--path',
                             metavar='--p',
                             type=str,
                             help='the Input file path for guardrail.ini')
    return func_parser.parse_args(args) 

@staticmethod
def validate_return(val, message, guardrail):
    """
    Function to validate the returns from subprocess

    Parameters:
      val (int): return value from subprocess
      message (string): message to be printed.
      guardrail (bool): identifier whether a process or guardrail gate.

    Returns:
    sub-process return value.
    """
    process = "" if guardrail else "task"
    if val:
        msg = "Guardrail {}, failed {}.".format(process, message)
        LOG.info(msg)  # pragma: no mutate
        sys.exit(val)
    else:
        msg = "Guardrail {}, passed {}.".format(process, message)
        LOG.info(msg)  # pragma: no mutate
        return
