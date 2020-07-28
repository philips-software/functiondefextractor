"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
file to verify the functional tests."""

import os
import sys
import unittest

sys.path.append(os.path.dirname(__file__))
from test.test_core_extractor import SimpleTest  # pylint: disable=C0413


class FunctionalTestVerification(unittest.TestCase):
    """
    class consolidates the functional test verification
    """
    file_path = (os.path.join(os.path.dirname(__file__), os.pardir)).split("test")[0]

    def verify_functional_test(self):
        """ This function verifies the result populated from the functional test """
        SimpleTest.test_process_extract(self)
