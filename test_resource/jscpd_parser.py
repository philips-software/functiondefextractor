""" This file process the output of report of jscpd execution """
import sys
import argparse
import json


def create_parser(args):
    """ Function which add the command line arguments required for the jscpd report parser"""
    # Create the parser
    jscpd_parser = argparse.ArgumentParser(description='jscpd Parser')

    # Add the arguments
    jscpd_parser.add_argument('--json',
                            metavar='--j',
                            type=int,
                            help='jscpd benchmark')
    return jscpd_parser.parse_args(args)


def parse_jscpd_report_json(duplicate_limit):
    """ Function to judge if JSCPD gating pass/fail"""
    with open('jscpd-report.json', 'rb') as data_file:
        data = json.load(data_file)
        per = float(data['statistics']['total']['percentage'])
    if per <= float(duplicate_limit):
        print("Passed jscpd gating")
        sys.exit(0)
    else:
        print("Failed jscpd gating")
        sys.exit(1)


if __name__ == '__main__':
    """ Entry function for jscpd parser"""
    # Execute the parse_args() method
    ARGS = create_parser(sys.argv[1:])
    # Process the cosine with inputs provided
    parse_jscpd_report_json(ARGS.json)
