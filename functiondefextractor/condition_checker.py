"""This file contains a function required for patterns in the extracted method/function definitions
based on given condition"""
import os

import excel2img
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
    data.to_excel(os.path.join(os.path.dirname(file_path), 'Pattern_Result_%s.xlsx') % condition.strip("@"))
    get_pivot_table_result(data, test_assert, splitter, file_path)


def get_pivot_table_result(data, test_assert, splitter, file_path):
    if splitter is not None:
        data["%s Statements" % test_assert] = data["%s Statements" % test_assert].apply(lambda x: x.split(splitter)[0])
    data_table = data.groupby("%s Statements" % test_assert).count().iloc[:, 1]
    if data_table.index[0] == '':
        data_table = data_table.drop([data_table.index[0]])
    data_table = data_table.to_frame()
    data_table = data_table.rename({'Count of %s in function' % test_assert:
                                        'Different %s pattern counts' % test_assert}, axis='columns')
    writer = pd.ExcelWriter('pivot_table.xlsx')
    data_table.to_excel(writer, sheet_name='sheetName', index=True, na_rep='NaN')
    [writer.sheets['sheetName'].set_column(i, i, len('Different %s pattern counts' % test_assert)) for i in range(2)]
    writer.save()
    excel2img.export_img(r"pivot_table.xlsx", os.path.join(os.path.dirname(file_path),
                                                           'Pivot_table_%s.png' % test_assert), "sheetName", None)
    os.remove('pivot_table.xlsx')


check_condition("assert", r"C:\Users\320074769\Downloads\funcDefExtractResult_18-32-03_01_07_2020_test.xlsx", "(")
