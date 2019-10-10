
import re
from pathlib import Path
import os


# TODO: Move
r"""

D:\a\1\s\Src\SelfTest\SelfTest_Errors.c: In function 'SelfTest_Errors_MemFault':
D:\a\1\s\Src\SelfTest\SelfTest_Errors.c:98:31: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
     uint32_t * wrongPointer = (uint32_t *)constValue; /* Set pointer address to an incorrect address */
                               ^
"""

# For regex use the
# https://regex101.com/r/0rW3Bo/1/
COMPILER_WARNING_CHECKERS = [
    {
        "CompilerName": "MSVC",
        "AutoDetect": None,
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


# TODO: Simplier solution
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


def check_files(file_list=None, compiler="MSVC"):

    if file_list is None:
        # Check all logs
        for filename in Path("..").glob("**/*.log"):
            print("Filename: {}".format(filename))
            #filepath = os.path.join("..", filename)
            with open(filename, "r") as file:
                file_content = file.read()
                warning_list = check_text(text=file_content, compiler=compiler)
                # Filter
                warning_list = warning_filter(warning_list)

                warning_string = "".join("    " + str(item) + "\n" for item in warning_list)
                if len(warning_string) != 0:
                    print("Found warning(s) at file: '{}'\n"
                          "{}".format(
                                filename, warning_string))
                else:
                    print("Not found warning at file '{}'".format(filename))
    else:
        # TODO: has file_list
        raise Exception("Not implemented")


if __name__== "__main__":
    local_mode = False

    # TODO: Beautify
    if local_mode:
        warning_example_text = \
r"""
C:\Program Files (x86)\Windows Kits\10\Include\10.0.17763.0\ucrt\stdio.h(948,37): warning C4710:  'int printf(const char *const ,...)': function not inlined [D:\a\1\s\Out\CMakeBuild\FastenHomeAut.vcxproj]
  EventHandler.c
  EventLog.c
  GlobalVarHandler.c
  HomeAutMessage.c
"""
        check_text(warning_example_text, "MSVC")
    else:
        # Pipeline mode
        check_files()

