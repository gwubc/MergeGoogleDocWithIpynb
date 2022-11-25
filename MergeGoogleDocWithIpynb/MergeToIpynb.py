import nbformat

from MergeGoogleDocWithIpynb.CodeResourceContainer import CodeResourceContainer
from MergeGoogleDocWithIpynb.MdResourceContainer import MdResourceContainer, BlockType


class MergeToIpynb:
    mdResource: MdResourceContainer = None
    codeResource: CodeResourceContainer = None

    def __init__(self, mdResource: MdResourceContainer, codeResource: CodeResourceContainer):
        self.mdResource = mdResource
        self.codeResource = codeResource

    def generate(self, outPath):
        codeData = self.codeResource.getAnalyseCodeCells()
        parts = self.mdResource.getAnalysedTextBlock()

        nb = nbformat.v4.new_notebook()
        nb['cells'] = []

        for t, p in parts:
            if t == BlockType.MD:
                nb['cells'].append(nbformat.v4.new_markdown_cell(p))

            elif t == BlockType.CODE:
                codeTxt = codeData.get(p)
                if not codeTxt:
                    codeTxt = "# Code Not Found"
                codeCell = nbformat.v4.new_code_cell(codeTxt)
                codeCell["attachments"] = {"id": {"id": p}}
                nb['cells'].append(codeCell)

            else:
                pass

        if outPath is not None:
            nbformat.write(nb, outPath)
        return nb
