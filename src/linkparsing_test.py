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
from linkparsing import GccLinkParserProvider

class LinkParserTest(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser()
        self.p.add_parser_provider(GccLinkParserProvider())

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
        self.assertEquals(len(links), 6, 'incorrect nr of links')
        lnk = links[2]
        self.assertEquals(lnk.path, 'test.c', 'incorrect path')
        self.assertEquals(lnk.line_nr, 11, 'incorrect line nr')
        self.assertEquals(gcc_output[lnk.start:lnk.end], 'test.c:11',
                            'the link positions are incorrect')

    def test_parse_gcc_one_line(self):
        links = self.p.parse("/tmp/myfile.c:1212: error: ...")
        self.assertEquals(len(links), 1, 'incorrect nr of links')
        lnk = links[0]
        self.assertEquals(lnk.path, '/tmp/myfile.c', 'incorrect path')
        self.assertEquals(lnk.line_nr, 1212, 'incorrect line nr')
        self.assertEquals(lnk.start, 0, 'incorrect start point')
        self.assertEquals(lnk.end, 18, 'incorrect start point')

    def test_parse_gcc_empty_string(self):
        links = self.p.parse("")
        self.assertEquals(len(links), 0, 'incorrect nr of links')

    def test_parse_gcc_no_files_in_text(self):
        links = self.p.parse("no file links in this string")
        self.assertEquals(len(links), 0, 'incorrect nr of links')

    def test_parse_gcc_none_as_argument(self):
        self.assertRaises(ValueError, self.p.parse, None)


if __name__ == '__main__':
    unittest.main()

