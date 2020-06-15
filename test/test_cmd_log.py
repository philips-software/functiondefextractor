""" This file does the  test of the "Text similarity processor
logging and commandline """

import unittest
import os
import subprocess
import filecmp
from test.test_resource import TestResource
from extractor_cmd import create_parser


def check_create_parser(option, value):
    """ create a parser for commandline input and return handle"""
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

    def test_delts(self):
        """ Function to test the annotation condition variable in the command line """
        with self.assertRaises(SystemExit):
            check_create_parser("-d", "delta_value")
        parsed = check_create_parser("--d", "delta_value")
        self.assertEqual(parsed.delta, "delta_value")

    def test_from_command_help(self):
        """Test function to test the commandline help option"""
        script = os.path.abspath(os.path.join(TestResource.par_dir, "functiondefextractor",
                                              "extractor_cmd.py"))
        cmd = 'python %s --h' % script
        output = open(os.path.join(TestResource.tst_resource_folder, "cmd_help.txt"), "r")
        tmpfile = open(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"), "w")
        subprocess.Popen(cmd, stdout=tmpfile, shell=True).communicate()[0]
        tmpfile.close()
        output.close()
        self.assertEqual(True, (filecmp.cmp(os.path.join(TestResource.tst_resource_folder, "cmd_help.txt"),
                                            os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"))),
                         "Help option validated")
        if os.path.exists(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt")):
            os.remove(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"))

    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_validate_inputs(self):
        """Test function to test the validate_inputs function"""
        script = os.path.abspath(os.path.join(TestResource.par_dir, "functiondefextractor",
                                              "extractor_cmd.py"))
        cmd = 'python %s --p %s' %(script, os.path.join(TestResource.tst_resource_folder, "wrong"))
        output = open(os.path.join(TestResource.tst_resource_folder, "cmd_validate.txt"), "r")
        tmpfile = open(os.path.join(TestResource.tst_resource_folder, "tmp_validate.txt"), "w")
        subprocess.Popen(cmd, stdout=tmpfile, shell=True).communicate()[0]
        tmpfile.close()
        output.close()
        self.assertEqual(True, (filecmp.cmp(os.path.join(TestResource.tst_resource_folder, "cmd_validate.txt"),
                                            os.path.join(TestResource.tst_resource_folder, "tmp_validate.txt"))),
                         "validate_inputs function validated")
        if os.path.exists(os.path.join(TestResource.tst_resource_folder, "tmp_validate.txt")):
            os.remove(os.path.join(TestResource.tst_resource_folder, "tmp_validate.txt"))


if __name__ == '__main__':
    unittest.main()
