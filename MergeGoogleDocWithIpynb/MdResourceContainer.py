from enum import Enum
from typing import List

from MergeGoogleDocWithIpynb.Utility import Utility

class BlockType(Enum):
    CODE = 1
    MD = 2
    NEWBLOCK = 3
    OTHER = 4

class MdResourceContainer:
    _rawTxt = ''
    removeLeadingTrailingBlankLine = True

    def __init__(self):
        pass

    def add(self, s):
        if self._rawTxt != "":
            self._rawTxt += "\n{%%}\n"
        self._rawTxt += s

    def _isComment(self, s) -> bool:
        s = Utility.standardizeStr(s)
        if len(s) > 4 and s[:2] == "{#" and s[-2:] == "#}":
            return True
        return False

    def _isNewTextBlock(self, s) -> bool:
        s = Utility.standardizeStr(s)
        if s == "{%newtextblock%}" or s == "{%%}":
            return True
        return False

    def _isCodePlaceholder(self, s) -> bool:
        s = s.replace(" ", '').lower()
        if len(s) > 4 and "{{" == s[:2] and "}}" == s[-2:]:
            return True
        return False

    def _analyseRawTxt(self) -> List[tuple[BlockType, str]]:
        txtParts = []
        for line in self._rawTxt.split('\n'):
            if self._isNewTextBlock(line):
                txtParts.append((BlockType.NEWBLOCK, ""))
            elif self._isCodePlaceholder(line):
                txtParts.append((BlockType.CODE, Utility.getCodeCellId(line[2:-2])))
            elif self._isComment(line):
                pass
            else:
                txtParts.append((BlockType.MD, line))
        return txtParts

    def _mergeTextBlock(self, txtParts: List[tuple[BlockType, str]]) -> List[tuple[BlockType, str]]:
        parts = []
        for t, l in txtParts:
            if t == BlockType.CODE:
                parts.append((BlockType.CODE, l))
            elif t == BlockType.NEWBLOCK:
                parts.append((BlockType.NEWBLOCK, ''))
            elif t == BlockType.MD:
                if len(parts):
                    if parts[-1][0] == BlockType.MD:
                        parts[-1] = (BlockType.MD, parts[-1][1] + "\n" + l)
                    else:
                        parts.append((BlockType.MD, l))
                else:
                    parts.append((BlockType.MD, l))
            else:  # BlockType.OTHER
                pass

        return parts

    def _removeLeadingTrailingBlankLineForEachTxtPart(self, parts: List[tuple[BlockType, str]]) -> List[tuple[BlockType, str]]:
        for i in range(len(parts)):
            t, l = parts[i]
            if t == BlockType.MD:
                parts[i] = (BlockType.MD, l.strip())
        return parts

    def getAnalysedTextBlock(self) -> List[tuple[BlockType, str]]:
        s = self._mergeTextBlock(self._analyseRawTxt())
        if self.removeLeadingTrailingBlankLine:
            s = self._removeLeadingTrailingBlankLineForEachTxtPart(s)
        return s

