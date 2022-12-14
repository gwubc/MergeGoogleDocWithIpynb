import nbformat
from jinja2 import Environment, BaseLoader

from MergeGoogleDocWithIpynb.Types import BlockType, MarkdownResource, CodeResource


class MergeToIpynb:

    markdownResource: MarkdownResource = None
    codeResource: CodeResource = None
    def __init__(self):
        self.markdownResource = []
        self.codeResource = {}

    def addMarkdownResource(self, markdownResource: MarkdownResource):
        self.markdownResource += markdownResource

    def addCodeResource(self, codeResource: CodeResource):
        self.codeResource.update(codeResource)

    def generate(self, outPath, **data):
        nb = nbformat.v4.new_notebook()
        nb['cells'] = []

        for t, p in self.markdownResource:
            if t == BlockType.MD:
                if data:
                    rtemplate = Environment(loader=BaseLoader).from_string(p)
                    res = rtemplate.render(**data)
                else:
                    res = p

                nb['cells'].append(nbformat.v4.new_markdown_cell(res))

            elif t == BlockType.CODE:
                codeTxt = self.codeResource.get(p)
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
