# -*- coding: utf-8 -*-
#    Gedit External Tools plugin
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

    def __init__(self, path, line_nr):
        self._path = path
        self._line_nr = line_nr

class LinkParser:

    def __init__(self):
        self._providers = [
            GccLinkParserProvider()
        ]

    def parse(self, line):
        link = None

        for provider in self._providers:
            lnk = provider.parse(line)
            if lnk is not None:
                link = lnk

        return link

class LinkParserProvider:

    def parse(self, line):
        raise NotImplementedError("need to implement a parse method")

class GccLinkParserProvider(LinkParserProvider):

    def __init__(self):
        self.fm = re.compile("^(.*)\:(\d+)\:", re.MULTILINE)

    def parse(self, line):
        for m in re.finditer(self.fm, line):
            print "%s %s" % (m.group(1), m.group(2))
        
        print line
        return None


