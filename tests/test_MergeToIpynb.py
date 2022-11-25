import unittest

import nbformat

from MergeGoogleDocWithIpynb.CodeResourceContainer import CodeResourceContainer
from MergeGoogleDocWithIpynb.MdResourceContainer import MdResourceContainer
from MergeGoogleDocWithIpynb.MergeToIpynb import MergeToIpynb
from MergeGoogleDocWithIpynb.ResourceCollector import ResourceCollector, ResourceType


class test_MergeToIpynb(unittest.TestCase):

    def test_generate(self):
        outPath = './ResourceForTests/out1.ipynb'
        # outPath = None

        mdResourceCollector = ResourceCollector(ResourceType.MARKDOWN)
        mdResourceCollector.collectFromLocalFile("./ResourceForTests/markdown1.md")

        mdResourceContainer = MdResourceContainer()
        mdResourceContainer.add(mdResourceCollector.exportToMd())

        codeResourceCollector = ResourceCollector(ResourceType.IPYNB)
        codeResourceCollector.collectFromLocalFile("./ResourceForTests/codePart1.ipynb")

        codeResourceContainer = CodeResourceContainer()
        codeResourceContainer.codeBlockRemoveCellId = True
        codeResourceContainer.add(codeResourceCollector.exportToIpynb())

        mergeToIpynb = MergeToIpynb(mdResourceContainer, codeResourceContainer)

        actual = mergeToIpynb.generate(outPath)

        self.checkCorrectNotebook(actual)

        with open("./ResourceForTests/out1.ipynb", encoding='utf8') as f:
            saved = f.read()

        actualSaved = nbformat.reads(saved, as_version=4)
        self.checkCorrectNotebook(actualSaved)

    def test_generateWithCodeCannotFind(self):
        outPath = None

        mdResourceCollector = ResourceCollector(ResourceType.MARKDOWN)
        mdResourceCollector.collectFromLocalFile("./ResourceForTests/markdown4.md")

        mdResourceContainer = MdResourceContainer()
        mdResourceContainer.add(mdResourceCollector.exportToMd())

        codeResourceCollector = ResourceCollector(ResourceType.IPYNB)
        codeResourceCollector.collectFromLocalFile("./ResourceForTests/codePart1.ipynb")

        codeResourceContainer = CodeResourceContainer()
        codeResourceContainer.codeBlockRemoveCellId = True
        codeResourceContainer.add(codeResourceCollector.exportToIpynb())

        mergeToIpynb = MergeToIpynb(mdResourceContainer, codeResourceContainer)

        actual = mergeToIpynb.generate(outPath)
        cells = actual["cells"]
        self.assertEqual("markdown", cells[0]["cell_type"])
        self.assertEqual("## Title", cells[0]["source"])
        self.assertEqual("markdown", cells[1]["cell_type"])
        self.assertEqual("This is markdown 4", cells[1]["source"])
        self.assertEqual("code", cells[2]["cell_type"])
        self.assertEqual('# Code Not Found', cells[2]["source"])
        self.assertEqual('1_1000', cells[2]["attachments"]['id']['id'])
        self.assertEqual("markdown", cells[3]["cell_type"])
        self.assertEqual("End of markdown4", cells[3]["source"])

    def checkCorrectNotebook(self, actual):
        cells = actual["cells"]
        self.assertEqual("markdown", cells[0]["cell_type"])
        self.assertEqual("This is markdown 1", cells[0]["source"])
        self.assertEqual("code", cells[1]["cell_type"])
        self.assertEqual('print("This is from codePart1.ipynb")', cells[1]["source"])
        self.assertEqual('1', cells[1]["attachments"]['id']['id'])
        self.assertEqual("markdown", cells[2]["cell_type"])
        self.assertEqual("End of markdown1", cells[2]["source"])
