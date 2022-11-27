from MergeGoogleDocWithIpynb.Exception import ResourceAnalysisException
from MergeGoogleDocWithIpynb.ResourceAnalyzer import ResourceAnalyzer
from MergeGoogleDocWithIpynb.Types import ResourceType, MarkdownResource, BlockType
from MergeGoogleDocWithIpynb.Utility import Utility


class MarkdownResourceAnalyzer(ResourceAnalyzer):
    removeLeadingTrailingBlankLine = True

    def __init__(self, resourceType: ResourceType, rawResource: str):
        super().__init__(resourceType, rawResource)

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

    def _analyseRawTxt(self) -> MarkdownResource:
        txtParts = []
        for line in self.rawResource.split('\n'):
            if self._isNewTextBlock(line):
                txtParts.append((BlockType.NEWBLOCK, ""))
            elif self._isCodePlaceholder(line):
                txtParts.append((BlockType.CODE, Utility.getCodeCellId(line[2:-2])))
            elif self._isComment(line):
                pass
            else:
                txtParts.append((BlockType.MD, line))
        return txtParts

    def _mergeTextBlock(self, txtParts: MarkdownResource) -> MarkdownResource:
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

    def _removeLeadingTrailingBlankLineForEachTxtPart(self, parts: MarkdownResource) -> MarkdownResource:
        for i in range(len(parts)):
            t, l = parts[i]
            if t == BlockType.MD:
                parts[i] = (BlockType.MD, l.strip())
        return parts

    def analysis(self) -> MarkdownResource:
        if self.resourceType != ResourceType.MARKDOWN:
            raise ResourceAnalysisException(f"resourceType: {self.resourceType}, currently not supported")

        s = self._mergeTextBlock(self._analyseRawTxt())
        if self.removeLeadingTrailingBlankLine:
            s = self._removeLeadingTrailingBlankLineForEachTxtPart(s)
        return s
