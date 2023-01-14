
import re
from pathlib import Path
import os
import argparse
import csv


# For regex use the
# https://regex101.com/
COMPILER_WARNING_CHECKERS = [
    {
        "CompilerName": "MSVC",
        "AutoDetect": None,
        # https://regex101.com/r/0rW3Bo/2/
        "WarningChecker": r" *(?P<FilePath>[\:\\\/\w \(\)\_\-\.]+)[\\|\/](?P<FileName>[\w\_\-]+\.[\w]*)\((?P<LineNumber>[\d]+),(?P<ColumnIndex>[\d]+)\)\: warning C(?P<WarningId>[\d]+)\: (?P<WarningMessage>[^[]*)\[",
        "ExampleText": [
            r"""
            MSVC
            C:\Program Files (x86)\Windows Kits\10\Include\10.0.17763.0\ucrt\stdio.h(948,37): warning C4710:  'int printf(const char *const ,...)': function not inlined [D:\a\1\s\Out\CMakeBuild\FastenHomeAut.vcxproj]
              EventHandler.c
              EventLog.c
              GlobalVarHandler.c
              HomeAutMessage.c
            """,
            r"""
            D:\a\1\s\Src\Communication\Communication.c(223,1): warning C4206:  nonstandard extension used: translation unit is empty [D:\a\1\s\Out\CMakeBuild\FastenHomeAut.vcxproj]
              WebpageHandler.c
              Display.c
              DisplayHandler.c
              DisplayImages.c
              Display_SSD1306.c
              Font12x8.c
              Generating Code...
            """
        ]
    },
    {
        "CompilerName": "GCC",
        "AutoDetect": None,
        # https://regex101.com/r/uu9hHU/1
        "WarningChecker": r" *(?P<FilePath>[\:\\\/\w \(\)\_\-\.]+)[\\|\/](?P<FileName>[\w\_\-]+\.[\w]*)\:(?P<LineNumber>[\d]+)\:(?P<ColumnIndex>[\d]+)\: warning\: (?P<WarningMessage>[^[]*) \[\-(?P<WarningId>[^[]+)\]",
        "ExampleText": [
r"""
D:\a\1\s\Src\SelfTest\SelfTest_Errors.c: In function 'SelfTest_Errors_MemFault':
D:\a\1\s\Src\SelfTest\SelfTest_Errors.c:98:31: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
     uint32_t * wrongPointer = (uint32_t *)constValue; /* Set pointer address to an incorrect address */
                               ^
""",
"""
D:\a\1\s\Src\Modules\EEPROM.c: In function 'EEPROM_Write':
D:\a\1\s\Src\Modules\EEPROM.c:85:18: warning: comparison is always false due to limited range of data type [-Wtype-limits]
     if ((address < EEPROM_ADDRESS_START) || ((address + size) > EEPROM_ADDRESS_END))
                  ^
"""
        ]
    },
    {
        # TODO: Now similar to GCC
        "CompilerName": "Clang",
        "AutoDetect": None,
        # https://regex101.com/r/ti6emr/1
        "WarningChecker": r" *(?P<FilePath>[\:\\\/\w \(\)\_\-\.]+)[\\|\/](?P<FileName>[\w\_\-]+\.[\w]*)\:(?P<LineNumber>[\d]+)\:(?P<ColumnIndex>[\d]+)\: warning\: (?P<WarningMessage>[^[]*) \[\-(?P<WarningId>[^[]+)\]",
        # TODO: Warning code part + column not handled
        "ExampleText":
        [
"""
/home/vsts/work/1/s/Src/Common/Handler/HomeAutMessage.c:216:45: warning: suggest braces around initialization of subobject [-Wmissing-braces]
    HomeAut_InformationType information = { 0 };
                                            ^
                                            {}
""",
"""
/home/vsts/work/1/s/Src/Common/Handler/HomeAutMessage.c:629:49: warning: suggest braces around initialization of subobject [-Wmissing-braces]
    HomeAut_InformationType testInformation = { 0 };
                                                ^
                                                {}
""",
"""
/home/vsts/work/1/s/Src/List/CommandList.c:700:31: warning: for loop has empty body [-Wempty-body]
    for (i = 0; i < 1000; i++);
                              ^
"""
        ]
    }
]

# These paths will be filtered out
FILTER_LIST = [
    r"C:\Program Files (x86)"
]


def check_text(text, compiler="MSVC", debug=False):

    # Find our compiler
    compiler_found = None
    for compiler_checker_item in COMPILER_WARNING_CHECKERS:
        if compiler == compiler_checker_item["CompilerName"]:
            compiler_found = compiler_checker_item
            break

    assert compiler_found

    regex_warning = re.compile(compiler_found["WarningChecker"])

    # TOOD: Delete
    #for i, line in self.__file_content_enumerated_list:
    #    result = regex_text_full_line.match(line)

    # Find warnings
    warning_list = []
    for m in regex_warning.finditer(text):
        # TODO: Debug code
        if debug:
            print(m.groupdict())
        warning_list.append(m.groupdict())

    return warning_list

    # TODO: delete or refactor
    """
    match = re.findall(regex_warning, text)

    if match:
        for oneMatch in match:
            line = oneMatch["Line"]
            print("Line: {}".format(line))
    """


# warning_item["FilePath"]
# warning_item["FileName"]
# warning_item["LineNumber"]
# warning_item["ColumnIndex"]
# warning_item["WarningId"]
# warning_item["WarningMessage"]


def get_short_warning_string(warning):
    file_path_with_file_name = os.path.join(warning["FilePath"], warning["FileName"])
    return "{FileFullPath}:{LineNumber}:{ColumnIndex} [{WarningId}]:'{WarningMessage}'".format(
        FileFullPath=file_path_with_file_name,
        LineNumber=warning["LineNumber"],
        ColumnIndex=warning["ColumnIndex"],
        WarningId=warning["WarningId"],
        WarningMessage=warning["WarningMessage"]
        )


# TODO: Simpler solution
def warning_filter(warning_list):
    warning_filtered_list = []
    for warning_item in warning_list:
        warning_file_path = os.path.normpath(warning_item["FilePath"])
        warning_filtered = False
        for filter_path in FILTER_LIST:
            filter_path_normalized = os.path.normpath(filter_path)
            if filter_path_normalized in warning_file_path:
                # Found in filter list
                print("Warning filtered out: {}".format(get_short_warning_string(warning_item)))
                warning_filtered = True
                break  # Found, not need to find next

        if not warning_filtered:
            warning_filtered_list.append(warning_item)

    return warning_filtered_list


def translate_relative_paths(warning_list):
    pass
    # TODO: Not too easy to check, what was the executing root at original log file
    #cwd = os.getcwd()
    # But this for the new executing situation
    # Idea: Try check all path, and find the common part?


def print_all_warning_as_list(warning_list):
    warning_list_in_string = ""
    for item in warning_list:
        warning_string = get_short_warning_string(item)
        print(warning_string)
        warning_list_in_string += warning_string
        warning_list_in_string += '\n'

    return warning_list_in_string


def print_all_warning_as_table(warning_list):
    # For automatic colum size
    #max(mylist, key=len)
    for warning in warning_list:
        file_path_with_file_name = os.path.join(warning["FilePath"], warning["FileName"])
        warning_string = "| {FileFullPath:80} | {LineNumber:4} | {ColumnIndex:3} | {WarningId:7} | {WarningMessage}".format(
            FileFullPath=file_path_with_file_name,
            LineNumber=warning["LineNumber"],
            ColumnIndex=warning["ColumnIndex"],
            WarningId=warning["WarningId"],
            WarningMessage=warning["WarningMessage"]
            )
        print(warning_string)


def export_to_text_file(export_filename, warning_list):
    if len(warning_list) != 0:
        print("Found warning(s) at files:")
        # warning_string = "".join("    " + str(item) + "\n" for item in warning_list)
        # print("Found warning(s) at file: '{}'\n"
        #     "{}".format(
        #            filename, warning_string))
        print("-" * 120)
        warning_list_in_string = print_all_warning_as_list(warning_list)
        print("-" * 120)
        print_all_warning_as_table(warning_list)
        print("-" * 120)

        with open(export_filename, "w+") as export_file:
            export_file.write(warning_list_in_string)
            print("Warnings exported to '{}'".format(export_filename))
    else:
        print("Not found warning at file '{}'".format(export_filename))
        # TODO: Temporary solution for creating empty file (do not fail pipeline at artifacting)
        open(export_filename, 'a').close()


def export_to_csv(export_filename, warning_list):
    workspace_directory = os.getenv("Build.Repository.LocalPath", None)
    # Azure workspaces
    removing_workspace_directories = [r"/home/vsts/work/1/s/", "D:\\a\\1\\s\\"]
    # Update dictionary keys
    new_warn_list = []
    for i in warning_list:
        new_item = {}
        for k, v in i.items():
            if k == 'FilePath':
                new_item['Dir'] = v
            elif k == 'LineNumber':
                new_item['Line'] = v
            elif k == 'ColumnIndex':
                new_item['Col'] = v
            elif k == 'WarningId':  # Same name
                new_item['WarningId'] = v
            elif k == 'WarningMessage':  # Same name
                new_item['WarningMessage'] = v
        new_warn_list.append(new_item)
    # Create CSV
    with open(export_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Dir", "FileName", "Line", "Col", "WarnId", "WarningMessage"]
        if new_warn_list:
            # Cross-check the header length
            assert len(warning_list[0]) == len(fieldnames)
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in new_warn_list:
            # Update fields
            #if workspace_directory:
            for remove_workspace in removing_workspace_directories:
                if row["Dir"].startswith(remove_workspace):
                    row["Dir"] = row["Dir"].replace(remove_workspace, "")  # Remove unnecessary start part
                    break
            # Save fields
            writer.writerow(row)
        print("Warnings exported to '{}'".format(export_filename))


def check_files(file_list=None, compiler="MSVC"):

    if file_list is None:
        file_list = "**/*.log"
        # Check all logs
    # else:  has file_list

    find_file_list = Path(".").glob(file_list)
    if not find_file_list:
        print("[ERROR] No log find!")
    for filename in find_file_list:
        print("Filename: {}".format(filename))
        #filepath = os.path.join("..", filename)
        with open(filename, "r") as file:
            file_content = file.read()
            warning_list = check_text(text=file_content, compiler=compiler)
            # Filter
            warning_list = warning_filter(warning_list)

            # TODO: Relative path
            export_filename = os.path.splitext(filename)[0] + "_found_warnings.txt"
            export_to_text_file(export_filename, warning_list)

            export_filename = os.path.splitext(filename)[0] + "_found_warnings.csv"
            export_to_csv(export_filename, warning_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-fl", "--file_list", help="List of analyzing files", default="**/*.log")
    parser.add_argument("-cmp", "--compiler", help="Compiler", default="MSVC")

    args = parser.parse_args()
    check_files(file_list=args.file_list, compiler=args.compiler)

