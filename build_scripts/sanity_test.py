"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
script to conduct sanity test"""
import os
import unittest
import sys
from test.verify_path import FunctionalTestVerification  # pylint: disable=E0401
from subprocess_calls import call_subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "test"))


class SanityTestVerification(unittest.TestCase):
    """
    class to consolidate the sanity tests
    """
    verify_func_obj = FunctionalTestVerification()
    file_path = (os.path.join(os.path.dirname(__file__), os.pardir)).split("test")[0]

    def test_execute_sanity_suite(self):
        """
        Function which executes the sanity test
        """
        input_file = os.path.join(self.file_path, "test_resource", "test_repo")
        call_subprocess('python3 -m functiondefextractor.extractor_cmd --p "%s"' % input_file)
        self.verify_func_obj.verify_functional_test()
        print("Sanity test is COMPLETED & PASSED")


if __name__ == '__main__':
    unittest.main()
