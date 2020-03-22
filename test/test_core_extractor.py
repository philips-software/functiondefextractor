""" This file holds the unit test cases """
import unittest
import os
from test.test_resource import TestResource
import pandas as pd
from functiondefextractor.core_extractor import get_file_names
from functiondefextractor.core_extractor import get_function_names
from functiondefextractor.core_extractor import get_func_body
from functiondefextractor.core_extractor import extractor


class SimpleTest(unittest.TestCase):
    """Class to run unit test cases on the function definition extractor"""
    src_files = os.path.join(TestResource.tst_resource_folder, "test_repo", "src")

    def test_get_file_names(self):
        """Function to test get_file_names method"""
        files = get_file_names(self.src_files)
        expected = [os.path.join(self.src_files, "HelloController.java"), os.path.join(self.src_files, "test_c.c"),
                    os.path.join(self.src_files, "test_repo.java"), os.path.join(self.src_files, "test_cpp_code.cpp")]
        self.assertEqual(expected.sort(), files.sort())

    def test_get_function_names(self):
        """Function to test get_function_names method"""
        func, line_num = get_function_names(os.path.join(self.src_files, "HelloController.java"))
        expec_func = ['index1', 'index2', 'meth']
        expec_line_num = ['61', '67', '29']
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

    def test_process_ft(self):
        """Function to test the complete end to end process of function definition extractor (False True)"""
        file_path = (os.path.join(os.path.dirname(__file__), os.pardir)).split("test")[0]
        dataframe = extractor((os.path.join(file_path, "test_resource", "test_repo")), "False", "True",
                              None, None)
        self.__write_xlsx(dataframe, "expeccodeextractor_F_T")
        df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "expeccodeextractor_F_T.xlsx")).values.tolist()
        df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "codeextractor_F_T.xlsx")).values.tolist()
        self.assertEqual(df1_list, df2_list)

    def test_process_tf(self):
        """Function to test the complete end to end process of function definition extractor (True False)"""
        dataframe = extractor((os.path.join(file_path, "test_resource", "test_repo")), "True", "False",
                              None, None)
        # print(dataframe1)
        self.__write_xlsx(dataframe, "expeccodeextractor_T_F")
        df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "expeccodeextractor_T_F.xlsx")).values.tolist()
        df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "codeextractor_T_F.xlsx")).values.tolist()
        self.assertEqual(df1_list, df2_list)

    def test_process_ttad(self):
        """Function to test the complete end to end process of function definition extractor (True True Annotation
        delta)"""
        dataframe = extractor((os.path.join(file_path, "test_resource", "test_repo")), "True", "True",
                              "@Test", "5")
        self.__write_xlsx(dataframe, "expeccodeextractor_T_T_A_D")
        df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "expeccodeextractor_T_T_A_D.xlsx")).sort_values('Uniq ID').values.tolist()
        df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "codeextractor_T_T_A_D.xlsx")).sort_values('Uniq ID').values.tolist()
        self.assertEqual(df1_list, df2_list)

    def test_process_tta(self):
        """Function to test the complete end to end process of function definition extractor (True False annotation)"""
        dataframe = extractor((os.path.join(file_path, "test_resource", "test_repo")), "True", "True",
                              "@Test", None)
        self.__write_xlsx(dataframe, "expeccodeextractor_T_T_A")
        df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "expeccodeextractor_T_T_A.xlsx")).sort_values('Uniq ID').values.tolist()
        df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "codeextractor_T_T_A.xlsx")).sort_values('Uniq ID').values.tolist()
        self.assertEqual(df1_list, df2_list)

    def test_process_tt(self):
        """Function to test the complete end to end process of function definition extractor (True True)"""
        dataframe = extractor((os.path.join(file_path, "test_resource", "test_repo")), "True", "True",
                              None, None)

        self.__write_xlsx(dataframe, "expeccodeextractor_T_T")
        df1_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "expeccodeextractor_T_T.xlsx")).sort_values('Uniq ID').values.tolist()
        df2_list = pd.read_excel(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource",
                                              "codeextractor_T_T.xlsx")).sort_values('Uniq ID').values.tolist()
        self.assertEqual(df1_list, df2_list)

    def test_invalid_path(self):
        """Function to test valid input path"""
        self.assertEqual(extractor(os.path.join("abc", "sdr")), "Enter valid path")


if __name__ == '__main__':
    unittest.main()
