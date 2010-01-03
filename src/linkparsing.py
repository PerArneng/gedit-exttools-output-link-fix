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

import re

class Link:
    """
    This class represents a file link from within a string given by the
    output of some software tool.
    """

    def __init__(self, path, line_nr, start, end):
        """
        path -- the path of the file (that could be extracted)
        line_nr -- the line nr of the specified file
        start -- the index within the string that the link starts at
        end -- the index within the string where the link ends at
        """
        self.path    = path
        self.line_nr = int(line_nr)
        self.start   = start
        self.end     = end

    def __repr__(self):
        return "%s[%s](%s:%s)" % (self.path, self.line_nr, 
                                  self.start, self.end)

class LinkParser:
    """
    Parses a text using different parsing providers with the goal of finding one
    or more file links within the text. A typicak example could be the output
    from a compiler that specifies an error in a specific file. The path of the
    file, the line nr and some more info is then returned so that it can be used
    to be able to navigate from the error output in to the specific file.

    The actual work of parsing the text is done by instances of classes that
    inherits from AbstractLinkParser or by regular expressions. To add a new
    parser just create a class that inherits from AbstractLinkParser and then
    register in this class cunstructor using the method add_parser. If you want
    to add a regular expression then just call add_regexp in this class
    constructor and provide your regexp string as argument.
    """

    def __init__(self):
        self._providers = []
        self.add_regexp("^(.*)\:(\d+)\: (warning|error|note)") # gcc
        self.add_parser(PythonLinkParser())
        self.add_regexp("^(.*\.java)\:(\d+)\: ") # javac

    def add_parser(self, parser):
        self._providers.append(parser)

    def add_regexp(self, regexp):
        self._providers.append(RegexpLinkParser(regexp))

    def parse(self, text):
        """
        Parses the given text and returns a list of links that are parsed from
        the text. This method delegates to parser providers that can parse
        output from different kinds of formats. If no links are found then an
        empty list is returned.

        text -- the text to scan for file links. 'text' can not be None.
        """
        if text is None:
            raise ValueError("text can not be None")

        links = []

        for provider in self._providers:
            links.extend(provider.parse(text))

        return links

class AbstractLinkParser(object):
    """The "abstract" base class for link parses"""

    def parse(self, text):
        """
        This method should be implemented by subclasses. It takes a text as
        argument (never None) and then returns a list of Link objects. If no
        links are found then an empty list is expected. The Link class is
        defined in this module. If you do not override this method then a
        NotImplementedError will be thrown. 

        text -- the text to parse. This argument is never None.
        """
        raise NotImplementedError("need to implement a parse method")

class RegexpLinkParser(AbstractLinkParser):
    """
    A class that represents parsers that only use one single regular expression.
    It can be used by subclasses or by itself. See the constructor documentation
    for details about the rules surrouning the regexp.
    """

    def __init__(self, regex):
        """
        Creates a new RegexpLinkParser based on the given regular expression.
        It is important that the 1:st capturing group of the regular expression
        contains the path and that the 2:nd capturing group contains the line
        number.
        """
        self.re = re.compile(regex, re.MULTILINE)

    def parse(self, text):
        links = []
        for m in re.finditer(self.re, text):
            path = m.group(1)
            line_nr = m.group(2)
            start = m.start(1)
            end = m.end(2)
            link = Link(path, line_nr, start, end)
            links.append(link)

        return links

class PythonLinkParser(RegexpLinkParser):

    def __init__(self):
        # example: '  File "test.py", line 10, in <module>'
        super(PythonLinkParser, self).__init__(
                                       "^  File \"([^\"]+)\", line (\d+),")

    def parse(self, text):
        """
        Parse with the help of the regular expression but make sure that the
        link also includes the initial " character so it looks nice.
        """
        links = super(PythonLinkParser, self).parse(text)

        for lnk in links:
            lnk.start = lnk.start - 1

        return links

# ex:ts=4:et:
