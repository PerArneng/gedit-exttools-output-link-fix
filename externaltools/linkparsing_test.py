
import unittest
from linkparsing import LinkParser

class LinkParserTest(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser()

    def test_parse_gcc_simple(self):
        self.p.parse("test.c:12: error: sometext")

if __name__ == '__main__':
    unittest.main()

