# def get_function_names(file_names):
# #     """ Function to get method/function names from files
# #         @parameters
# #         file_names: Path to the file
# #         @return
# #         This function returns function/method names and line numbers of all the given files"""
# #     file_ext = str(os.path.basename(file_names).split('.')[1])
# #     find = "function" if file_ext.upper() == "CPP" or file_ext.upper() == "C" or file_ext.upper() == "PY" else "method"
# #     function_list = []
# #     line_numbers = []
# #     cmd = "ctags -x " + file_names + "| grep %s " % find
# #     proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# #     process = str(proc.stdout.read(), 'utf-8')
# #     process_list = re.findall(r'\w+', process)
# #     val = [index for index, value in enumerate(process_list) if value == find]
# #     [function_list.append(process_list[val[i] - 1]) for i in range(len(val))]
# #     [line_numbers.append(process_list[val[i] + 1]) for i in range(len(val))]
# #     return function_list, line_numbers
import os
#
# print(os.sep)
# val = r'mypython -m vulture C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\functiondefextractor ' \
#               r'C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test  --exclude C:\Projects\PythonRepo' \
#               r'\python_sample\FunctionDefExtractor\test --min-confidence 100 >C:\Projects\PythonRepo' \
#               r'\REPORT\deadcode.txt'
# val = val.replace('\\', "$")
# str = "@annot"
# if "ann" in str:
#     print("val")
file = r"C:\Users\320074769\AppData\Local\Programs\Python\Python37\Lib\site-packages\pandas\core\algorithms.py"
print(os.path.splitext(file)[1].upper())