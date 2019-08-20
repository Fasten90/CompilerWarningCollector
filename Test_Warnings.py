import CompilerWarningCollector

import unittest


class MyTestCase(unittest.TestCase):
    def test_warnings_examples(self):
        # Test examples is okay or not

        for compiler in CompilerWarningCollector.COMPILER_WARNING_CHECKERS:
            text = "".join(compiler["ExampleText"])
            compiler_name = compiler["CompilerName"]
            warning_list = CompilerWarningCollector.check_text(text, compiler_name)
            self.assertEqual(len(compiler["ExampleText"]), len(warning_list))

    # TODO: Test: empty file at check_files()


if __name__ == '__main__':
    unittest.main()
