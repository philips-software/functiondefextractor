"""This file contains a function required for patterns in the extracted method/function definitions
based on given condition"""
import os

import pandas as pd


def check_condition(condition, file_path, splitter=None):
    """ This function does the pattern match check, line containing the pattern will be extracted to output
        and also number of occurances in the specific function code
        @parameters
        condition: pattern key word (Ex: @staticmethod, @Test, etc.)
        file_path: Input xlsx file used for searching pattern"""
    extension = os.path.splitext(file_path)
    if extension[1].upper() != ".XLSX":
        return "Enter Valid Excel File"
    test_assert = condition
    data = pd.read_excel(file_path)
    if ['Uniq ID'] not in data.columns.ravel():
        return "Couldn't find vaild data"
    data = pd.DataFrame(data, columns=['Uniq ID', 'Code']).set_index("Uniq ID")
    specifier_column = []
    spe_data = ""
    for i in range(len(data)):
        for line in str(data.iat[i, 0]).splitlines():
            if test_assert.upper() in line.strip().upper():
                spe_data = spe_data + line.strip() + os.linesep
        specifier_column.append(spe_data)
        spe_data = ""
    data['Count of %s in function' % test_assert] = data["Code"].str.upper().str.count(test_assert.upper())
    data["%s Statements" % test_assert] = specifier_column
    get_pivot_table_result(data, test_assert, splitter, file_path)


def get_pivot_table_result(data, test_assert, splitter, file_path):
    """ This function creates a pivot table for easy analysis
        and also number of occurances in the specific function code
        @parameters
        data: generated pattern dataframe
        test_assert: pattern key word (Ex: @staticmethod, @Test, etc.)
        splitter: key to split statement in pivot table
        file_path: Input xlsx file used for searching pattern"""
    if splitter is not None:
        data["%s Statements" % test_assert] = data["%s Statements" % test_assert].apply(lambda x: x.split(splitter)[0])
    data_table = data.groupby("%s Statements" % test_assert).count().iloc[:, 1]
    if data_table.index[0] == '':
        data_table = data_table.drop([data_table.index[0]])
    data_table = data_table.to_frame()
    data_table = data_table.rename({'Count of %s in function' % test_assert:
                                        'Different %s pattern counts' % test_assert}, axis='columns')
    html_file_path = os.path.join(os.path.dirname(file_path), 'Pivot_table_%s.html') % test_assert.strip("@")
    writer = pd.ExcelWriter(os.path.join(os.path.dirname(file_path), 'Pattern_Result_%s.xlsx')
                            % test_assert.strip("@"), engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Data')
    data_table.to_excel(writer, sheet_name='Pivot Table')
    data_table = data_table.rename_axis(None)
    data_table.to_html(html_file_path)
    writer.save()
