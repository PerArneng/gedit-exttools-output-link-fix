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

import os
import gio

class FileLookup:

    def __init__(self):
        self.providers = []

    def add_provider(self, provider):
        self.providers.append(provider)

    def lookup(self, path):
        found_file = None
        for provider in self.providers:
            found_file = provider.lookup(path)
            if found_file is not None:
                break
                
        return found_file

class FileLookupProvider:
    
    def lookup(self, path):
        """
        xxxx
        """
        raise NotImplementedError("need to implement a lookup method")


class AbsoluteFileLookupProvider(FileLookupProvider):
    
    def lookup(self, path):
        if os.path.isabs(path) and os.path.isfile(path):
            return gio.File(path)
        else:
            return None

