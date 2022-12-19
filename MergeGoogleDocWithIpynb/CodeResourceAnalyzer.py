import nbformat

from MergeGoogleDocWithIpynb.Exception import ResourceAnalysisException
from MergeGoogleDocWithIpynb.ResourceAnalyzer import ResourceAnalyzer
from MergeGoogleDocWithIpynb.Types import ResourceType, CodeResource
from MergeGoogleDocWithIpynb.Utility import Utility


class CodeResourceAnalyzer(ResourceAnalyzer):
    codeBlockRemoveCellId = False
    _codeCells = None

    def __init__(self, resourceType: ResourceType, rawResource: str):
        super().__init__(resourceType, rawResource)
        self._codeCells = []

        if resourceType == ResourceType.IPYNB:
            nbSource = nbformat.reads(rawResource, as_version=4)
            for e, c in enumerate(nbSource.cells):
                if c['cell_type'] != "code":
                    continue
                self._codeCells.append(c)
        else:
            raise ResourceAnalysisException(f"resourceType: {resourceType}, currently not supported")

    def _getCodeIdForCell(self, c):
        firstLine = Utility.standardizeStr(c['source'].split('\n')[0])
        return Utility.getCodeCellId(firstLine)

    def _removeFirstLine(self, s):
        return '\n'.join(s.split('\n')[1:])

    def _analyseCodeCells(self) -> CodeResource:
        codeData: CodeResource = {}

        for c in self._codeCells:

            codeId = self._getCodeIdForCell(c)

            if not codeId:
                continue

            if self.codeBlockRemoveCellId:
                codeData[codeId] = self._removeFirstLine(c['source'])
            else:
                codeData[codeId] = c['source']

        return codeData

    def analysis(self) -> CodeResource:
        return self._analyseCodeCells()

    def findJsonData(self) -> str:
        for c in self._codeCells[::-1]:
            firstLine = Utility.standardizeStr(c['source'].split('\n')[0])
            if firstLine == "#data":
                return c["outputs"][0]['text']