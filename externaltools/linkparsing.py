
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
    
    def parse(self, line):
        print line
        return None


