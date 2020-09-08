"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import sys

from condition_checker import check_condition
from core_extractor import extractor
from core_extractor import get_report
from extractor_cmd import validate_inputs
from extractor_cmd import create_parser

if __name__ == '__main__':
    # Execute the parse_args() method
    ARGS = create_parser(sys.argv[1:])
    if ARGS.delta is not None and ARGS.annot is None:
        print("delta(--d) should be in combination with annotation(--a)")  # pragma: no mutate
        raise SystemExit
    if ARGS.conditionchecker is None:
        validate_inputs(ARGS.path, "repository")
        ARGS.reportpath = ARGS.path if ARGS.reportpath is None else ARGS.reportpath
        validate_inputs(ARGS.reportpath, "report folder")
        get_report(extractor(ARGS.path, ARGS.annot, ARGS.delta, ARGS.funcstartwith, ARGS.reportpath, ARGS.ignorefiles)
                   , ARGS.reportpath)
    else:
        validate_inputs(ARGS.excelfilepath, "Excel file")  # pragma: no mutate
        check_condition(ARGS.conditionchecker, ARGS.excelfilepath, ARGS.splitter)
