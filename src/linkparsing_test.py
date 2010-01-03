# -*- coding: utf-8 -*-
#
#    Copyright (C) 2009-2010  Per Arneng <per.arneng@anyplanet.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import unittest
from linkparsing import LinkParser

class LinkParserTest(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser()

    def assert_link_count(self, links, expected_count):
        self.assertEquals(len(links), expected_count, 'incorrect nr of links')

    def assert_link(self, actual, path, line_nr):
        self.assertEquals(actual.path, path, "incorrect path")
        self.assertEquals(actual.line_nr, line_nr, "incorrect line nr")

    def assert_link_text(self, text, link, link_text):
        self.assertEquals(text[link.start:link.end], link_text,
           "the expected link text does not match the text within the string")

    def test_parse_gcc_simple_test_with_real_output(self):
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
        links = self.p.parse(gcc_output)
        self.assert_link_count(links, 6)
        lnk = links[2]
        self.assert_link(lnk, "test.c", 11)
        self.assert_link_text(gcc_output, lnk, "test.c:11")

    def test_parse_gcc_one_line(self):
        line = "/tmp/myfile.c:1212: error: ..."
        links = self.p.parse(line)
        self.assert_link_count(links, 1)
        lnk = links[0]
        self.assert_link(lnk, "/tmp/myfile.c", 1212)
        self.assert_link_text(line, lnk, "/tmp/myfile.c:1212")

    def test_parse_gcc_empty_string(self):
        links = self.p.parse("")
        self.assert_link_count(links, 0)

    def test_parse_gcc_no_files_in_text(self):
        links = self.p.parse("no file links in this string")
        self.assert_link_count(links, 0)

    def test_parse_gcc_none_as_argument(self):
        self.assertRaises(ValueError, self.p.parse, None)

    def test_parse_python_simple_test_with_real_output(self):
        output = """
Traceback (most recent call last):
  File "test.py", line 10, in <module>
    err()
  File "test.py", line 7, in err
    real_err()
  File "test.py", line 4, in real_err
    int('xxx')
ValueError: invalid literal for int() with base 10: 'xxx'
"""
        links = self.p.parse(output)
        self.assert_link_count(links, 3)
        lnk = links[2]
        self.assert_link(lnk, "test.py", 4)
        self.assert_link_text(output, lnk, '"test.py", line 4')

    def test_parse_python_one_line(self):
        line = "  File \"test.py\", line 10, in <module>"
        links = self.p.parse(line)
        self.assert_link_count(links, 1)
        lnk = links[0]
        self.assert_link(lnk, "test.py", 10)
        self.assert_link_text(line, lnk, '"test.py", line 10')

    def test_parse_javac_one_line(self):
        line = "/tmp/Test.java:10: incompatible types"
        links = self.p.parse(line)
        self.assert_link_count(links, 1)
        lnk = links[0]
        self.assert_link(lnk, "/tmp/Test.java", 10)
        self.assert_link_text(line, lnk, '/tmp/Test.java:10')

    def test_parse_valac_simple_test_with_real_output(self):
        output = """
Test.vala:14.13-14.21: error: Assignment: Cannot convert from `string' to `int'
        int a = "xxx";
            ^^^^^^^^^
"""
        links = self.p.parse(output)
        self.assert_link_count(links, 1)
        lnk = links[0]
        self.assert_link(lnk, "Test.vala", 14)
        self.assert_link_text(output, lnk, 'Test.vala:14.13-14.21') 


if __name__ == '__main__':
    unittest.main()

# ex:ts=4:et:
