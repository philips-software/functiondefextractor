""" File provide command line interface for the text similarity index processor """
import argparse
import os
import subprocess
import sys

from condition_checker import check_condition
from core_extractor import extractor
from core_extractor import get_report
from core_extractor import LOG


def create_parser(args):
    """ Function which add the command line arguments required for the command line input
    of function definition extractor """
    # Create the parser
    func_parser = argparse.ArgumentParser(description='Function Definition Extractor')

    # Add the arguments
    func_parser.add_argument('--path',
                             metavar='--p',
                             type=str,
                             help='the Input folder path')

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

    func_parser.add_argument('--funcstartwith',
                             metavar='--f',
                             type=str,
                             default=None,
                             help='functions starting with given key word')

    func_parser.add_argument('--reportpath',
                             metavar='--r',
                             type=str,
                             default=None,
                             help='Input report folder path')

    func_parser.add_argument('--excelfilepath',
                             metavar='--e',
                             type=str,
                             default=None,
                             help='Input excel file path')

    func_parser.add_argument('--conditionchecker',
                             metavar='--c',
                             type=str,
                             default=None,
                             help='condition to analyse against extracted methods')

    func_parser.add_argument('--splitter',
                             metavar='--s',
                             type=str,
                             default=None,
                             help='key to split the extracted statements to generate a pivot table for easy analysis')

    # ...Create your parser as you like...
    return func_parser.parse_args(args)


def validate_inputs(arg_path, repo):
    """This function helps in validating the user inputs"""
    status_path = True if os.path.splitext(arg_path)[1].upper() == ".XLSX" and os.path.exists(arg_path) \
        else False if repo == "Excel file" else os.path.exists(arg_path)
    if status_path:
        LOG.info("Input path validated")  # pragma: no mutate
    if not status_path:
        LOG.info("Enter valid %s path" % repo)  # pragma: no mutate
        print("Enter valid %s path" % repo)  # pragma: no mutate
        sys.stdout.flush()
        script = os.path.abspath(os.path.join(os.path.realpath(__file__)))
        cmd = 'python %s --h' % script
        subprocess.call(cmd, shell=True)  # pragma: no mutate
        sys.exit(1)  # pragma: no mutate


if __name__ == '__main__':
    # Execute the parse_args() method
    ARGS = create_parser(sys.argv[1:])
    if ARGS.delta is not None and ARGS.annot is None:
        print("delta(--d) should be in combination with annotation(--a)")  # pragma: no mutate
        raise SystemExit
    if ARGS.conditionchecker is None:
        validate_inputs(ARGS.path, "repository")
        ARGS.reportpath = ARGS.path if ARGS.reportpath is None else ARGS.reportpath
        validate_inputs(ARGS.reportpath, "report folder")  # pragma: no mutate
        get_report(extractor(ARGS.path, ARGS.annot, ARGS.delta, ARGS.funcstartwith, ARGS.reportpath)
                   , ARGS.reportpath)
    else:
        validate_inputs(ARGS.excelfilepath, "Excel file")
        check_condition(ARGS.conditionchecker, ARGS.excelfilepath, ARGS.splitter)
