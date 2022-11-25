from typing import List

import nbformat

from MergeGoogleDocWithIpynb.Utility import Utility


class CodeResourceContainer:
    _codeCells: List[dict[str, str]] = None
    codeBlockRemoveCellId = False

    def __init__(self):
        self._codeCells = []

    def add(self, notebookJson):
        nbSource = nbformat.reads(notebookJson, as_version=4)
        for e, c in enumerate(nbSource.cells):
            self._codeCells.append(c)

    def _getCodeIdForCell(self, c):
        firstLine = Utility.standardizeStr(c['source'].split('\n')[0])
        return Utility.getCodeCellId(firstLine)

    def _removeFirstLine(self, s):
        return '\n'.join(s.split('\n')[1:])

    def analyseCodeCells(self) -> dict[str, str]:
        codeData: dict[str, str] = {}

        for c in self._codeCells:
            if c['cell_type'] != "code":
                continue

            codeId = self._getCodeIdForCell(c)

            if not codeId:
                continue

            if self.codeBlockRemoveCellId:
                codeData[codeId] = self._removeFirstLine(c['source'])
            else:
                codeData[codeId] = c['source']

        return codeData

    def getAnalyseCodeCells(self) -> dict[str, str]:
        return self.analyseCodeCells()

