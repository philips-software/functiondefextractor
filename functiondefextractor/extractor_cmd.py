""" File provide command line interface for the text similarity index processor """
import os
import subprocess
import sys
import argparse
import pandas as pd
# sys.path.append(os.path.abspath(os.path.join
#                                 (os.path.dirname(__file__), os.pardir
#                                  )))
# from function_def_extractor import function_def_extractor
from functiondefextractor.core_extractor import extractor


def create_parser(args):
    """ Function which add the command line arguments required for the commandline input
    of function definition extractor """
    # Create the parser
    func_parser = argparse.ArgumentParser(description='Function Definition Extractor')

    # Add the arguments
    func_parser.add_argument('--path',
                             metavar='--p',
                             type=str,
                             help='the Input folder path')

    func_parser.add_argument('--code',
                             metavar='--c',
                             type=str,
                             default="true",
                             help='True/False for source code to be processed?')

    func_parser.add_argument('--test',
                             metavar='--t',
                             type=str,
                             default="true",
                             help='True/False for test code to be processed?')

    func_parser.add_argument('--annot',
                             metavar='--a',
                             type=str,
                             default=None,
                             help='Annotation condition to get function/method definitions')

    func_parser.add_argument('--delta',
                             metavar='--d',
                             type=str,
                             default=None,
                             help='Required number of lines at annotated method')

    # ...Create your parser as you like...
    return func_parser.parse_args(args)


def validate_inputs(arg_path):
    """This function helps in validating the user inputs"""
    status_path = os.path.exists(arg_path)
    if not status_path:
        print("Enter Valid Path")
        sys.stdout.flush()
        script = os.path.abspath(os.path.join(os.path.realpath(__file__)))
        cmd = 'python %s --h' % script
        subprocess.Popen(cmd).communicate()[0]
        raise SystemExit


if __name__ == '__main__':
    # Execute the parse_args() method
    ARGS = create_parser(sys.argv[1:])
    validate_inputs(ARGS.path)
    # Process the similarity with inputs provided
    DATA_FR = extractor(ARGS.path, ARGS.code, ARGS.test, ARGS.annot, ARGS.delta)
    WRITER = pd.ExcelWriter('%s.xlsx' % os.path.join(ARGS.path, "funcDefExtractResult"), engine='xlsxwriter')
    DATA_FR.to_excel(WRITER, sheet_name="funcDefExtractResult")
    WRITER.save()
