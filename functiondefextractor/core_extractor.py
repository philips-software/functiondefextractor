"""This file contains all the functions required for extracting method/function definitions from the given repository"""
import subprocess
import os
import re
import pandas as pd

DELTA_BODY = []
UID_LIST = []


def get_file_names(dir_path):
    """ Function used for getting all the valid file names from the given directory
        @parameters
        dir_path: Path to the repository
        @return
        This function returns all the files in the given directory"""
    listoffile = os.listdir(dir_path)
    allfiles = list()
    for entry in listoffile:
        fullpath = os.path.join(dir_path, entry)
        if os.path.isdir(fullpath):
            allfiles = allfiles + get_file_names(fullpath)
        else:
            allfiles.append(fullpath)
    return allfiles


def get_function_names(file_names):
    """ Function to get method/function names from the input files in the given repo
        @parameters
        file_names: Path to the file
        @return
        This function returns function/method names and line numbers of all the given files"""
    file_ext = str(os.path.basename(file_names).split('.')[1])
    find = "function" if file_ext.upper() == "CPP" or file_ext.upper() == "C" else ["member", "function", "class"] \
        if file_ext.upper() == "PY" else "method"
    if find == ["member", "function", "class"]:
        cmd = "ctags -x " + file_names
    else:
        cmd = "ctags -x " + file_names + "| grep %s " % find
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return process_function_names(proc, find)


def process_function_names(func_data, find):
    """ This function cleans the ctags output to get function/method names and line numbers
        @parameters
        func_data: Ctags output
        find: keyword of method type(member/function/class/method)
        @return
        This function returns list of function names and line numbers"""
    process = str(func_data.stdout.read(), 'utf-8')
    process_list = re.findall(r'\w+', process)
    val = [index for index, value in enumerate(process_list) if
           process_list[index - 1] in find and process_list[index].isdigit()]
    function_list = get_sorted_func_list(process_list, val)
    line_numbers = get_func_line_num_list(process_list, val)
    line_numbers.sort()
    return function_list, line_numbers


def get_sorted_func_list(process_list, val):
    """ This function sorts function names with respective to line numbers
        @parameters
        process_list: Ctags output in list format
        val: filtered variable to get function name
        @return
        This function returns list of sorted function names based on line numbers"""
    return [val for _, val in
            sorted(zip(get_func_line_num_list(process_list, val), get_func_list(process_list, val)))]


def get_func_list(process_list, val):
    """ This function refines the ctags output to get function names
        @parameters
        process_list: Ctags output in list format
        val: filtered variable to get function name
        @return
        This function returns list of function"""
    function_list = []
    [function_list.append(process_list[val[i] - 2]) for i in range(len(val))]
    return function_list


def get_func_line_num_list(process_list, val):
    """ This function refines the ctags output to get function line numbers
        @parameters
        process_list: Ctags output in list format
        val: filtered variable to get function name
        @return
        This function returns list of function line numbers"""
    line_numbers = []
    [line_numbers.append(int(process_list[val[i]])) for i in range(len(val))]
    return line_numbers


def check_annot(filename, line_num, annot):
    """ Function checks for the annotation condition
        @parameters
        filename: Path to the file
        line_num: function/method line number
        annot: Annotation condition (Ex: @Test)
        @return
        This function returns function/method definitions that has the given annotation"""
    if annot is None:
        return get_func_body(filename, line_num)
    else:
        return get_annot_methods(filename, line_num, annot)


def get_file_content(filename):
    """ Function reads the given file
        @parameters
        filename: Path to the file
        @return
        This function returns content of the file inputed"""
    with open(filename) as file_data:
        return file_data.readlines()


def get_annot_methods(filename, line_num, annot):
    """ This function gets the methods that have given annotation
        @parameters
        filename: Path to the file
        line_num: function/method line number
        annot: Annotation condition (Ex: @Test)
        @return
        This function returns function/method definitions that has the given annotation"""
    file_content = get_file_content(filename)
    iterator = int(line_num) - 2
    for _ in range(int(line_num) - 2):
        data = str(file_content[iterator]).strip().upper()
        iterator = iterator - 1
        ret_val = process_annot_method_body(annot, data, filename, line_num)
        if ret_val != "continue":
            return ret_val


def process_annot_method_body(annot, data, filename, line_num):
    """ This function process the function/method to check if it has the given annotation
        @parameters
        filename: Path to the file
        line_num: function/method line number
        annot: Annotation condition (Ex: @Test)
        data: Content of the given file
        @return
        This function returns function/method definitions that has the given annotation"""
    ret_val = "continue"
    if annot.upper() in data.upper():
        ret_val = get_func_body(filename, line_num)
    elif data[:1] is not "@" and "}" in data or "{" in data:
        ret_val = None
    return ret_val


def check_py_annot(file_name, annot):
    """ Function checks for the annotation condition in python files
        @parameters
        filename: Path to the file
        annot: Annotation condition (Ex: @Test)
        @return
        This function returns function/method names that has the given annotation"""
    line_data = list([line.rstrip() for line in open(file_name)])
    data = []
    val = 0
    if annot == "test_":
        annot = "def test_"
        val = -1
    for i, _ in enumerate(line_data):
        if annot in line_data[i]:
            func_name = line_data[i + 1 + val].strip().split(" ")[1].split("(")[0]
            data.append(func_name)
    return data


def get_func_body(filename, line_num):
    """ Function to get method/function body from files
        @parameters
        filename, line_num: Path to the file, function/method line number
        @return
        This function returns function/method definitions of all the given files"""
    line_num = int(line_num)
    code = ""
    cnt_braket = 0
    found_start = False

    with open(filename, "r") as files:
        for i, line in enumerate(files):
            if i >= (line_num - 1):
                code += line

                if line.count("{") > 0:
                    found_start = True
                    cnt_braket += line.count("{")

                if line.count("}") > 0:
                    cnt_braket -= line.count("}")

                if cnt_braket == 0 and found_start is True:
                    return code


def get_py_func_body(line_numbers, file_name, annot):
    """ Function to get method/function body from files
        @parameters
        filename: Path to the file
        line_num: function/method line number
        annot: Annotation condition (Ex: @Test)
        @return
        This function returns python function/method definitions in the given files"""
    line_data = list([line.rstrip() for line in open(file_name)])
    data, data_func_name = process_py_methods(file_name, line_numbers, line_data)
    if annot is not None:
        data_func_name, data = get_py_annot_methods(file_name, data_func_name, data, annot)
    if len(data_func_name).__trunc__() != 0:
        return process_py_func_body(data, data_func_name)
    else:
        return [], []


def process_py_methods(file_name, line_numbers, line_data):
    """ This Function refines the python function names to remove any class or lamida functions
        @parameters
        filename: Path to the file
        line_num: function/method line number
        line_data: File content in list format
        @return
        This function returns processed python function/method names and definitions in the given files"""
    data = []
    data_func_name = []
    for i, _ in enumerate(line_numbers):
        start = line_numbers[i]
        stop = len(line_data) if i == len(line_numbers) - 1 else line_numbers[i + 1] - 1
        data.append("\n".join(line_data[start - 1:stop]))
        data_func_name.append(
            str(os.path.basename(file_name)) + "_" + str(line_data[start - 1].strip().split(" ")[1].split("(")[0]))
        if data[len(data) - 1].startswith("class") or "lambda" in data[len(data) - 1]:
            data.remove(data[len(data) - 1])
            data_func_name.pop(len(data_func_name) - 1)
    return data, data_func_name


def get_py_annot_methods(file_name, data_func_name, data, annot):
    """ This function filters the python functions to get methods that have given annotation
        @parameters
        filename: Path to the file
        data_func_name: list of all function names in the file
        data: File content in list format
        annot: Annotation condition (Ex: @staticmethod)
        @return
        This function returns python function/method names and definitions that have the given annotation"""
    annot_meth_line_num = check_py_annot(file_name, annot)
    annot_meth_name = []
    annot_meth_body = []
    for k, _ in enumerate(annot_meth_line_num):
        for j, _ in enumerate(data_func_name):
            if str(annot_meth_line_num[k]) in str(data_func_name[j]):
                annot_meth_body.append(data[j])
                annot_meth_name.append(data_func_name[j])
                break
    return annot_meth_name, annot_meth_body


def process_py_func_body(data_body, data_name):
    """ This function processes the collected python function definitions to put then in a organized way
        @parameters
        data_body: list of all function definitions in the file
        data_name: list of all function names in the file
        @return
        This function returns python function/method definitions in a organized format"""
    for i, _ in enumerate(data_body):
        data_body[i] = os.linesep.join([s for s in str(data_body[i]).splitlines() if s])
    data_body = clean_py_methods(data_body)
    return data_name, data_body


def clean_py_methods(data_body):
    """ This function cleans the collected python function definitions to remove any junk content entered into method
        while collecting
        @parameters
        data_body: list of all function definitions in the file
        data_name: list of all function names in the file
        @return
        This function returns python function/method definitions in a organized format"""
    for j, _ in enumerate(data_body):
        data_list = list(str(data_body[j]).split('\n'))
        count = len(data_list[0]) - len(data_list[0].lstrip())
        i = 0
        for i, _ in enumerate(data_list):
            if i == len(data_list) - 1 or len(data_list[i + 1]) - len(data_list[i + 1].lstrip()) <= count:
                break
        del data_list[i + 1:]
        data_body[j] = str("\n".join(data_list))
    return data_body


def filter_files(list_files):
    """ Function to filter required files from list of all files
    @parameters
    list_files: List of all files that the given repository contains
    @return
    This function returns the list of required file(.java, .cpp, .c, .cs, .py) paths """
    ext = [".java", ".cpp", ".c", ".cs", ".py"]
    local_files = []
    for files in list_files:
        extension = os.path.splitext(files)
        if len(extension).__trunc__() > 0:
            if extension[1] in ext:
                local_files.append(files)
    return local_files


def __write_xlsx(data_f, name):
    """ Function which write the dataframe to xlsx
    @parameters
    data_f: content in dataframe format
    name: File name to name the xlsx file generated"""
    curr_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_path, name)
    writer = pd.ExcelWriter('%s.xlsx' % file_path, engine='xlsxwriter')
    data_f.to_excel(writer, sheet_name=name)
    writer.save()


def get_delta_lines(file_name, annot, delta):
    """ Function to get + and - delta number of lines from the annoted method/function
            @parameters
            filename, annot, delta: Path to the file, required annotation, required lines from method """
    line_data = list(filter(None, [line.rstrip() for line in open(file_name)]))
    data = []
    for num, line in enumerate(line_data, 1):
        process_delta_lines_body(annot, line, delta, num, line_data, data, file_name)
        data = []


def process_delta_lines_body(annot, line, delta, num, line_data, data, file_name):
    """ Function to get + and - delta number of lines from the annoted method/function
        @parameters
        file_name: Path to the file
        annot: Required annotation
        delta: Required lines from method
        line_data: File content in list format
        data: variable that holds delta lines data"""
    if annot.upper() in line.strip().upper():
        for i in range(0, (int(delta) * 2) + 1):
            if num - (int(delta) + 1) + i >= len(line_data):
                break
            data.append(line_data[num - (int(delta) + 1) + i])
        DELTA_BODY.append("\n".join(data))
        UID_LIST.append(os.path.basename(file_name) + "_")


def get_flat_list(data_list):
    """ Function that generates a list by merging a list of sub lists
        @parameters
        data_list: list of sub lists
        @return
        This function returns a flattened list"""
    flattened_list = []
    for val in data_list:
        if str(type(val)) != "<class 'list'>":
            flattened_list.append(val)
        if str(type(val)) == "<class 'list'>":
            for sub_val in val:
                flattened_list.append(sub_val)
    return flattened_list


def process_delta_lines_data():
    """ This function processes delta lines data to generate a dataframe
        @return
        This function returns a dataframe of delta lines data"""
    data = {'Uniq ID': UID_LIST, 'Code': DELTA_BODY}
    data_frame = pd.DataFrame(data)
    UID_LIST.clear()
    mask = data_frame['Uniq ID'].duplicated(keep=False)
    data_frame.loc[mask, 'Uniq ID'] += data_frame.groupby('Uniq ID').cumcount().add(1).astype(str)
    return data_frame.set_index("Uniq ID").sort_values('Uniq ID')


def process_final_data(code_list):
    """ This function processes function/method data to generate a dataframe
        @return
        This function returns a dataframe of function/method data"""
    flat_uid_list = get_flat_list(UID_LIST)
    flat_code_list = get_flat_list(code_list)
    data = {'Uniq ID': flat_uid_list, 'Code': flat_code_list}
    data_frame = pd.DataFrame.from_dict(data, orient='index')
    data_frame = data_frame.transpose()
    UID_LIST.clear()
    return data_frame.set_index("Uniq ID").sort_values('Uniq ID')


def process_py_files(code_list, line_num, func_name, annot):
    """ This function processes that input python files to extract methods from the given repo
        @parameters
        code_list: list to store the extracted methods
        line_num: list of function line numbers
        func_name: list of function names
        annot: given annotation condition (Ex: @staticmethod)
        @return
        This function returns extracted python methods"""
    if len(line_num).__trunc__() != 0:
        def_name, def_body = get_py_func_body(line_num, func_name, annot)
        if len(def_body).__trunc__() != 0:
            UID_LIST.append(def_name)
            code_list.append(def_body)
    return code_list


def process_input_files(line_num, functions, annot, func_name, code_list):
    """ This function processes that input files to extract methods from the given repo
        @parameters
        code_list: list to store the extracted methods
        line_num: list of function line numbers
        func_name: list of function names
        annot: given annotation condition (Ex: @staticmethod)
        @return
        This function returns extracted python methods"""
    for lin_no, func in zip(line_num, functions):
        if check_annot(func_name, lin_no, annot) is not None:
            code_list.append(check_annot(func_name, lin_no, annot))
            UID_LIST.append(os.path.basename(func_name) + "_" + func)
    return code_list


def get_final_dataframe(delta, code_list):
    """ This function processes extracted data to generate a dataframe
         @parameters
        code_list: list of extracted methods
        delta: Required lines from method
        @return
        This function returns a dataframe of extracted function/methods"""
    if delta is not None:
        ret_val = process_delta_lines_data()
    else:
        ret_val = process_final_data(code_list)
    return ret_val


def extractor(path_loc, annot=None, delta=None):
    """ Function that initiates the overall process of extracting function/method definitions from the files
        @parameters
        path_loc: directory path of the repository
        annot: given annotation condition (Ex: @staticmethod, @Test)
        delta: Required lines from method
        @return
        This function returns a data frame which contains the function/method names and body
        of the processed input files
        @usage
        function_def_extractor(path to repo, "@test")
        the above function call initiates the process to run function definition extraction on
        all files with @test annotation of the repository given """
    if not os.path.exists(path_loc):
        print("Enter valid path")
        return "Enter valid path"
    code_list = []
    for func_name in filter_files(get_file_names(path_loc)):
        if delta is not None:
            get_delta_lines(func_name, annot, delta)
        else:
            functions, line_num = get_function_names(func_name)
            if os.path.splitext(func_name)[1].upper() == ".PY":
                code_list = process_py_files(code_list, line_num, func_name, annot)
            else:
                code_list = process_input_files(line_num, functions, annot, func_name, code_list)
    return get_final_dataframe(delta, code_list)
