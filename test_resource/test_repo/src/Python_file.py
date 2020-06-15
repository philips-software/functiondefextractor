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