import types
import re


class DocString2Json(object):
    def __init__(self, raw_method):
        self.raw = self._docstring_init(raw_method)
        if not self.raw:
            return None
        self.rows = self.raw.split("\n")
        self.dict = {}
        for row in self.rows:
            self._add_row(row)

    def _docstring_init(self, raw_data):
        if type(raw_data) == types.StringType:
            return self._clear_docstring(raw_data)
        elif type(raw_data) == types.FunctionType:
            return self._clear_docstring(raw_data.__doc__)
        return None


    def _clear_docstring(self, string):
        return re.sub(r"^@json", "", string.strip()).strip()

    def _add_row(self, row):
        key = re.findall(r"@([a-zA-Z0-9_]+)?\s", row)[0]
        if not key in self.dict:
            self.dict[key] = []
        key_regex = r"^(\s+)?@{}\s".format(key)
        self.dict[key].append(re.sub(key_regex, "", row))

    def __iter__(self):
        for item in self.dict.items():
            yield item[0], item[1] if len(item[1]) > 1 else item[1][0]

