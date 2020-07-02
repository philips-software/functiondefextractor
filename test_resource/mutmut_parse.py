""" This file process the output of report of mutmut execution """
import sys
import argparse
import xml.etree.ElementTree as ET


def create_parser(args):
    """ Function which add the command line arguments required for the mutmut report parser"""
    # Create the parser
    mutmut_parser = argparse.ArgumentParser(description='Mutmut Parser')

    # Add the arguments
    mutmut_parser.add_argument('--mut',
                            metavar='--m',
                            type=int,
                            help='mutation benchmark')
    return mutmut_parser.parse_args(args)


def check_pass_fail(failure, total, allow_fail_per):
    """ Function which check the failure percentile against total mutation runs
    Exits successfully if actual failure is equal or less than the specified allowed failure"""
    per = int(total) * (allow_fail_per / 100)
    if failure <= per:
        print("passed Mutation testing")
        sys.exit(0)
    else:
        print("failed Mutation testing")
        sys.exit(1)


def parse_mutmut_report_xml(allow_fail):
    """ Function usd to fetch the necessary data from the xml output - mutmut"""
    try:
        root = ET.parse('mutmut.xml').getroot()
        disabled = int(root.get('disabled'))
        errors = int(root.get('errors'))
        failures = int(root.get('failures'))
        tests = int(root.get('tests'))
        total_fail = disabled+errors+failures
        print("Total Failure= %s || Total Tests= %s || Total Allowed percent fail= %s" % (total_fail, tests,
                                                                                          allow_fail))
        check_pass_fail(total_fail, tests, allow_fail)
    except FileNotFoundError:
        print("mutmut.xml report file path")


if __name__ == '__main__':
    """ Entry function for mutmut parser"""
    # Execute the parse_args() method
    ARGS = create_parser(sys.argv[1:])
    # Process the cosine with inputs provided
    parse_mutmut_report_xml(ARGS.mut)
