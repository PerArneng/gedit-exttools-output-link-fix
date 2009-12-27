
import unittest
from linkparsing import LinkParser

class LinkParserTest(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser()

    def test_parse_gcc_simple(self):
        gcc_output = """
test.c: In function 'f':
test.c:5: warning: passing argument 1 of 'f' makes integer from pointer without a cast
test.c:3: note: expected 'int' but argument is of type 'char *'
test.c: In function 'main':
test.c:11: warning: initialization makes pointer from integer without a cast
test.c:12: warning: initialization makes integer from pointer without a cast
test.c:13: error: too few arguments to function 'f'
test.c:14: error: expected ';' before 'return'
"""
        self.p.parse(gcc_output)

if __name__ == '__main__':
    unittest.main()

