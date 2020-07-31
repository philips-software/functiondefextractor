"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
file to verify the functional tests."""

import os
import unittest

import pandas as pd


class FunctionalTestVerification(unittest.TestCase):
    """
    class consolidates the functional test verification
    """
    def verify_functional_test(self):
        """ This function verifies the result populated from the functional test """
        my_dir = os.path.join(os.path.dirname(__file__), os.pardir, "test_resource")
        for fname in os.listdir(my_dir):
            if fname.startswith("ExtractedFunc_"):
                df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                                      fname)).sort_values('Uniq ID')
                df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                                      "codeextractor_T_T_A.xlsx")).sort_values('Uniq ID')
                df2_list["Code"] = df2_list["Code"].str.replace(os.linesep, "")
                df1_list["Code"] = df1_list["Code"].str.replace(os.linesep, "")
                df2_list["Code"] = df2_list["Code"].str.replace("\r", "")
                self.assertEqual(df1_list["Code"].values.tolist().sort(), df2_list["Code"].values.tolist().sort(),
                                 "Verifying two dataframes")
                os.remove(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", fname))
