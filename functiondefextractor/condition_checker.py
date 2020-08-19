"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import os

import pandas as pd
from pandas import DataFrame


def check_condition(condition, file_path_dataframe, splitter=None):
    """ This function does the pattern match check, line containing the pattern will be extracted to output
        and also number of occurrences in the specific function code
        @parameters
        condition: pattern key word (Ex: @staticmethod, @Test, etc.)
        file_path: Input xlsx file used for searching pattern"""
    if str(type(file_path_dataframe)) == "<class 'pandas.core.frame.DataFrame'>":
        data = file_path_dataframe
    else:
        extension = os.path.splitext(file_path_dataframe)
        if extension[1].upper() != ".XLSX":
            return "Enter Valid Excel File"
        data = pd.read_excel(file_path_dataframe)
    test_assert = condition
    if ['Uniq ID'] not in data.columns.ravel():
        return "Couldn't find Uniq ID column"
    data = pd.DataFrame(data, columns=['Uniq ID', 'Code'])
    specifier_column = []
    spe_data = ""
    for i in range(len(data)):
        for line in str(data.iat[i, 1]).splitlines():
            if test_assert.upper() in line.strip().upper():
                spe_data = spe_data + line.strip() + os.linesep
        specifier_column.append(spe_data)
        spe_data = ""
    data['Count of %s in function' % test_assert] = data["Code"].str.upper().str.count(test_assert.upper())
    data["%s Statements" % test_assert] = specifier_column
    return get_pivot_table_result(data, test_assert, splitter, file_path_dataframe)


def clean_data(splitter, data):
    """ This function is used to filter the data based on the splitter
        @parameters
        data: generated pattern dataframe
        splitter: key to split statement in pivot table"""
    specifier_column = []
    if splitter is not None:
        for i in range(len(data)):
            for line in str(data.iat[i, 3]).splitlines():
                specifier_column.append(line.split(splitter)[0])
    else:
        for i in range(len(data)):
            for line in str(data.iat[i, 3]).splitlines():
                specifier_column.append(line)
    return specifier_column


def get_pivot_table_result(data, test_assert, splitter, file_path):
    """ This function creates a pivot table for easy analysis
        and also number of occurrences in the specific function code
        @parameters
        data: generated pattern dataframe
        test_assert: pattern key word (Ex: @staticmethod, @Test, etc.)
        splitter: key to split statement in pivot table
        file_path: Input xlsx file used for searching pattern"""
    specifier_column = clean_data(splitter, data)
    data_frame = DataFrame(specifier_column, columns=['Count'])
    data_table = data_frame.Count.value_counts()
    data_table = data_table.to_frame()
    data_table = data_table.reset_index()
    data_table = data_table.rename({'index': 'Different %s patterns ' % test_assert}, axis='columns')
    if data_table.iat[0, 0] == '':  # pragma: no mutate
        data_table = data_table.drop([data_table.index[0]])  # pragma: no mutate
    if str(type(file_path)) != "<class 'pandas.core.frame.DataFrame'>":  # pragma: no mutate
        writer = pd.ExcelWriter(os.path.join(os.path.dirname(file_path), 'Pattern_Result_%s.xlsx')
                                % test_assert.strip("@"), engine='xlsxwriter')
        data.to_excel(writer, sheet_name='Data')  # pragma: no mutate
        html_file_path = os.path.join(os.path.dirname(file_path), 'Pivot_table_%s.html') % test_assert.strip("@")
        data_table.to_excel(writer, sheet_name='Pivot Table')  # pragma: no mutate
        data_table.to_html(html_file_path)
        writer.save()
        ret_val = "Report files successfully generated at input path"  # pragma: no mutate
    else:
        ret_val = data, data_table
    return ret_val
