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
    """ Function to get method/function names from files
        @parameters
        file_names: Path to the file
        @return
        This function returns function/method names and line numbers of all the given files"""
    file_ext = str(os.path.basename(file_names).split('.')[1])
    find = "function" if file_ext.upper() == "CPP" or file_ext.upper() == "C" else "method"
    function_list = []
    line_numbers = []
    cmd = "ctags -x " + file_names + "| grep %s " % find
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process = str(proc.stdout.read(), 'utf-8')
    process_list = re.findall(r'\w+', process)
    val = [index for index, value in enumerate(process_list) if value == find]
    [function_list.append(process_list[val[i] - 1]) for i in range(len(val))]
    [line_numbers.append(process_list[val[i] + 1]) for i in range(len(val))]
    return function_list, line_numbers


def check_annot(filename, line_num, annot):
    """ Function checks for the annotation condition
        @parameters
        filename, line_num: Path to the file, function/method line number
        @return
        This function returns function/method definitions of all the given files"""
    if annot is None:
        code = get_func_body(filename, line_num)
        return code
    else:
        with open(filename) as file_data:
            file_content = file_data.readlines()
            iterator = int(line_num) - 2
            # print(iterator)
            for _ in range(int(line_num) - 2):
                data = str(file_content[iterator]).strip().upper()
                iterator = iterator - 1
                if annot.upper() in data.upper():  # Change to start with
                    code = get_func_body(filename, line_num)
                    return code
                elif data[:1] is not "@" and "}" in data or "{" in data:
                    return None


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


def filter_files(list_files):
    """ Function to filter required files from list of all files
    @parameters
    list_files: List of all files that the given repository contains
    @return
    This function returns the list of required file(.java, .cpp, .c, .cs) paths """
    ext = [".java", ".cpp", ".c", ".cs"]
    local_files = []
    for files in list_files:
        extension = os.path.splitext(files)
        if extension[1] in ext:
            local_files.append(files)
    return local_files


def __write_xlsx(data_f, name):
    """ Function which write the dataframe to xlsx """
    curr_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_path, name)
    # Github open ticket for the abstract method
    writer = pd.ExcelWriter('%s.xlsx' % file_path, engine='xlsxwriter')
    data_f.to_excel(writer, sheet_name=name)
    writer.save()


def get_filtered_files(code, test, path_repo, annot):
    """ Function to filter required files(source code or test files) from list of all files
       @parameters
       code: Condition to select source code files
       test: Condition to select test files
       path_repo: path to repository
       @return
       This function returns the list of required file(Source/test files) """
    test_files = get_test_files(path_repo)
    final_files = []
    if annot is not None:
        return filter_files(get_file_names(path_repo))
    if code.upper() == "TRUE" and test.upper() == "TRUE":
        final_files = filter_files(get_file_names(path_repo))
    if code.upper() == "TRUE" and test.upper() == "FALSE":
        final_files = filter_files(list(set(get_file_names(path_repo)) ^ set(test_files)))
    if code.upper() == "FALSE" and test.upper() == "TRUE":
        final_files = filter_files(test_files)
    if code.upper() == "FALSE" and test.upper() == "FALSE":
        final_files = filter_files(get_file_names(path_repo))
    return final_files


def get_test_files(path_repo):
    """ Function to get test files from the list of all files
           @parameters
           path_repo: path to repository
           @return
           This function returns the list of test files"""
    test_files = []
    for file_paths in get_file_names(path_repo):
        split_path = file_paths.split(os.sep)
        for folder_name in split_path:
            if folder_name in ("test", "tst"):
                test_files.append(file_paths)
    return test_files


def get_delta_lines(file_name, annot, delta):
    """ Function to get + and - delta number of lines from the annoted method/function
            @parameters
            filename, annot, delta: Path to the file, required annotation, required lines from method """
    line_data = list(filter(None, [line.rstrip() for line in open(file_name)]))
    data = []
    for num, line in enumerate(line_data, 1):
        if annot.upper() in line.strip().upper():
            for i in range(0, (int(delta) * 2) + 1):
                if num - (int(delta) + 1) + i >= len(line_data):
                    break
                data.append(line_data[num - (int(delta) + 1) + i])
            DELTA_BODY.append("\n".join(data))
            UID_LIST.append(os.path.basename(file_name) + "_")
            data = []


def extractor(path_loc, parse_code="True", parse_test="True", annot=None, delta=None):
    """ Function that initiates the overall process of extracting function/method definitions from the files
    @parameters
    path_loc is directory path of the repository
    parse_code condition to process code files alone
    parse_test condition to process code test alone
    @return
    This function returns a data frame which contains the function/method names and body of the processed input files
    @usage
    function_def_extractor(path to repo, parse_code=True, parse_test=False)
    the above function call initiates the process to run function definition extraction on
    code files of the repository given """
    if not os.path.exists(path_loc):
        print("Enter valid path")
        return "Enter valid path"

    code_list = []
    for func_name in get_filtered_files(parse_code, parse_test, path_loc, annot):
        if delta is not None:
            get_delta_lines(func_name, annot, delta)

        else:
            functions, line_num = get_function_names(func_name)
            for lin_no, func in zip(line_num, functions):
                if check_annot(func_name, lin_no, annot) is not None:
                    code_list.append(check_annot(func_name, lin_no, annot))
                    UID_LIST.append(os.path.basename(func_name) + "_" + func)
    if delta is not None:
        data = {'Uniq ID': UID_LIST, 'Code': DELTA_BODY}
        data_frame = pd.DataFrame(data)
        UID_LIST.clear()
        mask = data_frame['Uniq ID'].duplicated(keep=False)
        data_frame.loc[mask, 'Uniq ID'] += data_frame.groupby('Uniq ID').cumcount().add(1).astype(str)
        return data_frame.set_index("Uniq ID").sort_values('Uniq ID')
    else:
        data = {'Uniq ID': UID_LIST, 'Code': code_list}
        data_frame = pd.DataFrame.from_dict(data, orient='index')
        data_frame = data_frame.transpose()
        UID_LIST.clear()
        return data_frame.set_index("Uniq ID").sort_values('Uniq ID')
