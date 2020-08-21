"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import unittest
import os
import subprocess
import filecmp
from test.test_resource import TestResource
from extractor_cmd import create_parser


def check_create_parser(option, value):
    """ create a parser for command line input and return handle"""
    return create_parser([option, value])


class ParserAndLogTest(unittest.TestCase):
    """ Class to test the logging and command line input feature """

    def test_path(self):
        """ Function to test the path variable in the command line
        correct and incorrect """
        with self.assertRaises(SystemExit):
            check_create_parser("-p", "path_test")
        parsed = check_create_parser("--p", "path_test")
        self.assertEqual(parsed.path, "path_test")

    def test_annot_condition(self):
        """ Function to test the annotation condition variable in the command line """
        with self.assertRaises(SystemExit):
            check_create_parser("-a", "annot_condition")
        parsed = check_create_parser("--a", "annot_condition")
        self.assertEqual(parsed.annot, "annot_condition")

    def test_delta(self):
        """ Function to test the annotation condition variable in the command line """
        with self.assertRaises(SystemExit):
            check_create_parser("-d", "delta_value")
        parsed = check_create_parser("--d", "delta_value")
        self.assertEqual(parsed.delta, "delta_value")

    def test_func_start_with(self):
        """ Function to test the function start with condition in the command line """
        with self.assertRaises(SystemExit):
            check_create_parser("-f", "func_start_with")
        parsed = check_create_parser("--p", "func_start_with")
        self.assertEqual(parsed.path, "func_start_with")

    def test_from_command_help(self):
        """Test function to test the command line help option"""
        script = os.path.abspath(os.path.join(TestResource.par_dir, "functiondefextractor"))
        cmd = 'python %s --h' % script
        output = open(os.path.join(TestResource.tst_resource_folder, "cmd_help.txt"), "r")
        tmpfile = open(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"), "w")
        subprocess.call(cmd, stdout=tmpfile, shell=True)
        tmpfile.close()
        output.close()
        self.assertEqual(True, (filecmp.cmp(os.path.join(TestResource.tst_resource_folder, "cmd_help.txt"),
                                            os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"))),
                         "Help option validated")
        if os.path.exists(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt")):
            os.remove(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"))

    def test_validate_inputs(self):
        """Test function to test the validate_inputs function"""
        script = os.path.abspath(os.path.join(TestResource.par_dir, "functiondefextractor",))
        cmd = 'python %s --p %s' % (script, os.path.join(TestResource.tst_resource_folder, "wrong"))
        output = open(os.path.join(TestResource.tst_resource_folder, "cmd_validate.txt"), "r")
        tmpfile = open(os.path.join(TestResource.tst_resource_folder, "tmp_validate.txt"), "w")
        subprocess.call(cmd, stdout=tmpfile, shell=True)
        tmpfile.close()
        output.close()
        self.assertEqual(True, (filecmp.cmp(os.path.join(TestResource.tst_resource_folder, "cmd_validate.txt"),
                                            os.path.join(TestResource.tst_resource_folder, "tmp_validate.txt"))),
                         "validate_inputs function validated")
        if os.path.exists(os.path.join(TestResource.tst_resource_folder, "tmp_validate.txt")):
            os.remove(os.path.join(TestResource.tst_resource_folder, "tmp_validate.txt"))


if __name__ == '__main__':
    unittest.main()
