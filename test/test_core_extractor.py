""" This file holds the unit test cases """
import unittest
import os
from test.test_resource import TestResource
import pandas as pd
from core_extractor import get_file_names
from core_extractor import get_function_names
from core_extractor import get_func_body
from core_extractor import extractor


class SimpleTest(unittest.TestCase):
    """Class to run unit test cases on the function definition extractor test"""
    src_files = os.path.join(TestResource.tst_resource_folder, "test_repo", "src")
    file_path = (os.path.join(os.path.dirname(__file__), os.pardir)).split("test")[0]

    def test_get_file_names(self):
        """Function to test get_file_names method"""
        files = get_file_names(self.src_files)
        expected = [os.path.join(self.src_files, "HelloController.java"), os.path.join(self.src_files, "test_c.c"),
                    os.path.join(self.src_files, "test_repo.java"), os.path.join(self.src_files, "test_cpp_code.cpp"),
                    os.path.join(self.src_files, "Python_annot_file.py"),
                    os.path.join(self.src_files, "Python_file.py")]
        self.assertEqual(expected.sort(), files.sort())

    def test_get_function_names(self):
        """Function to test get_function_names method"""
        func, line_num = get_function_names(os.path.join(self.src_files, "HelloController.java"))
        expec_func = ['meth', 'index1', 'index2']
        expec_line_num = [29, 61, 67]
        self.assertEqual(expec_func, func)
        self.assertEqual(expec_line_num, line_num)

    def test_get_func_body(self):
        """Function to test get_function_body method"""
        func_body = get_func_body(os.path.join(self.src_files, "CerberusTest.java"), '24')
        func_body_format = func_body.split()
        func_body_formated = ''.join(func_body_format)
        expec_func_body = "publicvoidafterAll(){super.restoreStreams();}"
        self.assertEqual(expec_func_body, func_body_formated)

    @staticmethod
    def get_formatted_data_frame(dataframe):
        """Function to format the data frame"""
        df_list = dataframe.values.tolist()
        process_data = ','.join(df_list[0])
        process_data_format = process_data.split()
        formated_data_frame = ''.join(process_data_format)
        return formated_data_frame

    @staticmethod
    def __write_xlsx(data_f, name):
        """ Function which write the dataframe to xlsx """
        curr_path = (
            os.path.join((os.path.join(os.path.dirname(__file__), os.pardir)).split("test")[0], "test_resource"))
        file_path = os.path.join(curr_path, name)
        writer = pd.ExcelWriter('%s.xlsx' % file_path, engine='xlsxwriter')
        data_f.to_excel(writer, sheet_name=name)
        writer.save()

    def test_process_ad(self):
        """Function to test the complete end to end process of function definition extractor with
        Annotation and delta)"""
        dataframe = extractor((os.path.join(self.file_path, "test_resource", "test_repo")), "@Test", "5")
        self.__write_xlsx(dataframe, "expeccodeextractor_T_T_A_D")
        df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "expeccodeextractor_T_T_A_D.xlsx")).sort_values('Uniq ID').values.tolist()
        df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "codeextractor_T_T_A_D.xlsx")).sort_values('Uniq ID').values.tolist()
        self.assertEqual(df1_list, df2_list)
        os.remove(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                               "expeccodeextractor_T_T_A_D.xlsx"))

    def test_process_extract(self):
        """Function to test the complete end to end process of function definition extractor (True False annotation)"""
        dataframe = extractor((os.path.join(self.file_path, "test_resource", "test_repo")), None, None)
        self.__write_xlsx(dataframe, "expeccodeextractor_T_T_A")
        df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "expeccodeextractor_T_T_A.xlsx")).sort_values('Uniq ID')
        df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "codeextractor_T_T_A.xlsx")).sort_values('Uniq ID')
        self.assertTrue(df1_list["Uniq ID"].equals(df2_list["Uniq ID"]))
        os.remove(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", "expeccodeextractor_T_T_A.xlsx"))

    def test_process_annot(self):
        """Function to test the complete end to end process of function definition extractor (True False annotation)"""
        dataframe = extractor((os.path.join(self.file_path, "test_resource", "test_repo")), "@Test", None)
        self.__write_xlsx(dataframe, "expeccodeextractor_annot")
        df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "expeccodeextractor_annot.xlsx")).sort_values('Uniq ID').values.tolist()
        df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "codeextractor_annot.xlsx")).sort_values('Uniq ID').values.tolist()
        self.assertEqual(df1_list, df2_list)
        os.remove(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", "expeccodeextractor_annot.xlsx"))

    def test_process_python_test_extract(self):
        """Function to test the complete end to end process of function definition extractor (True True)"""
        dataframe = extractor((os.path.join(self.file_path, "test_resource", "test_repo")), "test_", None)
        self.__write_xlsx(dataframe, "expeccodeextractor_T_T")
        df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "expeccodeextractor_T_T.xlsx")).sort_values('Uniq ID')
        df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "codeextractor_T_T.xlsx")).sort_values('Uniq ID')
        self.assertTrue(df1_list["Uniq ID"].equals(df2_list["Uniq ID"]))
        os.remove(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", "expeccodeextractor_T_T.xlsx"))

    def test_invalid_path(self):
        """Function to test valid input path"""
        self.assertEqual(extractor(os.path.join("abc", "sdr")), "Enter valid path")


if __name__ == '__main__':
    unittest.main()
