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

    def __init__(self, path, line_nr, start, end):
        self._path = path
        self._line_nr = line_nr
        self._start = start
        self._end = end

    def __repr__(self):
        return "%s[%s](%s:%s)" % (self._path, self._line_nr, 
                                  self._start, self._end)

class LinkParser:

    def __init__(self):
        self._providers = [
            GccLinkParserProvider()
        ]

    def parse(self, text):
        links = []

        for provider in self._providers:
            links.extend(provider.parse(text))

        return links

class LinkParserProvider:

    def parse(self, line):
        raise NotImplementedError("need to implement a parse method")

class GccLinkParserProvider(LinkParserProvider):

    def __init__(self):
        self.fm = re.compile("^(.*)\:(\d+)\:", re.MULTILINE)

    def parse(self, text):
        links = []
        for m in re.finditer(self.fm, text):
            path = m.group(1)
            line_nr = m.group(2)
            start = m.start(1)
            end = m.end(2)
            link = Link(path, line_nr, start, end)
            links.append(link)

        return links


