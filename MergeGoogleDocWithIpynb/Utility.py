import re


class Utility:

    @staticmethod
    def standardizeStr(s: str) -> str:
        return "".join(s.split()).lower().replace(".", "_")

    @staticmethod
    def getCodeCellId(s) -> str | None:
        s = Utility.standardizeStr(s)
        rePatten = '#?code:?([0-9|a-z]\w*)'
        if not re.match(rePatten, s):
            return None

        codeId = re.findall(rePatten, s)
        return codeId[0]
