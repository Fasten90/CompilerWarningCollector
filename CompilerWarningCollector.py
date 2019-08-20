
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


def check_text(text, compiler="MSVC"):
    regex_warning = re.compile(COMPILER_WARNING_CHECKERS[0]["WarningChecker"])

    # TOOD: Delete
    #for i, line in self.__file_content_enumerated_list:
    #    result = regex_text_full_line.match(line)

    warning_list = []
    for m in regex_warning.finditer(text):
        # TODO: Debug code
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


def check_files(file_list=None, compiler="MSVC"):

    if file_list is None:
        # Check all logs
        for filename in Path("..").glob("**/*.log"):
            print("Filename: {}".format(filename))
            #filepath = os.path.join("..", filename)
            with open(filename, "r") as file:
                file_content = file.read()
                warning_list = check_text(text=file_content)
                warning_string = "".join("    " + item for item in warning_list)
                if len(warning_string) != 0:
                    print("Found warning at file '{}'\n"
                          "{}".format(
                                filename, warning_string))
                else:
                    print("Not found warning at file '{}'".format(filename))

if __name__== "__main__":
    local_mode = False

    if local_mode:
        text = \
r"""
C:\Program Files (x86)\Windows Kits\10\Include\10.0.17763.0\ucrt\stdio.h(948,37): warning C4710:  'int printf(const char *const ,...)': function not inlined [D:\a\1\s\Out\CMakeBuild\FastenHomeAut.vcxproj]
  EventHandler.c
  EventLog.c
  GlobalVarHandler.c
  HomeAutMessage.c
"""
        check_text(text, "MSVC")
    else:
        # Pipeline mode
        check_files()

