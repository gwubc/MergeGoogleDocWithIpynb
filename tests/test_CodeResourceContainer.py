import unittest

from MergeGoogleDocWithIpynb.CodeResourceContainer import CodeResourceContainer
from MergeGoogleDocWithIpynb.ResourceCollector import ResourceType, ResourceCollector


class test_CodeResourceContainer(unittest.TestCase):
    codeResourceContainer = None
    resourceCollector1 = None

    def setUp(self) -> None:
        self.codeResourceContainer = CodeResourceContainer()
        self.resourceCollector1 = ResourceCollector(ResourceType.IPYNB)
        self.resourceCollector1.collectFromLocalFile("./ResourceForTests/codePart1.ipynb")

    def test_addOnce(self):
        self.codeResourceContainer.add(self.resourceCollector1.exportToIpynb())
        self.assertEqual(1, self.codeResourceContainer._codeCells.__len__())
        self.assertEqual([{'cell_type': 'code', 'execution_count': None, 'metadata': {'collapsed': True}, 'outputs': [],
                           'source': '# code 1\nprint("This is from codePart1.ipynb")'}],
                         self.codeResourceContainer._codeCells)

    def test_addTwice(self):
        self.codeResourceContainer.add(self.resourceCollector1.exportToIpynb())

        resourceCollector = ResourceCollector(ResourceType.IPYNB)
        resourceCollector.collectFromLocalFile("./ResourceForTests/codePart2.ipynb")
        self.codeResourceContainer.add(resourceCollector.exportToIpynb())

        expect = [{'cell_type': 'code',
                   'execution_count': None,
                   'metadata': {'collapsed': True},
                   'outputs': [],
                   'source': '# code 1\nprint("This is from codePart1.ipynb")'},
                  {'cell_type': 'code',
                   'execution_count': None,
                   'metadata': {'collapsed': True},
                   'outputs': [],
                   'source': '# code 2\nprint("This is from codePart2.ipynb")'}]

        self.assertEqual(2, self.codeResourceContainer._codeCells.__len__())
        self.assertEqual(expect, self.codeResourceContainer._codeCells)

    def test_getAnalyseCodeCellsOneCell(self):
        self.codeResourceContainer.add(self.resourceCollector1.exportToIpynb())
        self.assertEqual(1, self.codeResourceContainer.getAnalyseCodeCells().keys().__len__())
        self.assertEqual({'1': '# code 1\nprint("This is from codePart1.ipynb")'},
                         self.codeResourceContainer.getAnalyseCodeCells())

    def test_getAnalyseCodeCellsOneCellWithoutFirstLine(self):
        self.codeResourceContainer.add(self.resourceCollector1.exportToIpynb())
        self.codeResourceContainer.codeBlockRemoveCellId = True
        self.assertEqual(1, self.codeResourceContainer.getAnalyseCodeCells().keys().__len__())
        self.assertEqual({'1': 'print("This is from codePart1.ipynb")'},
                         self.codeResourceContainer.getAnalyseCodeCells())

    def test_getAnalyseCodeCellsTwoCell(self):
        self.codeResourceContainer.add(self.resourceCollector1.exportToIpynb())

        resourceCollector = ResourceCollector(ResourceType.IPYNB)
        resourceCollector.collectFromLocalFile("./ResourceForTests/codePart2.ipynb")
        self.codeResourceContainer.add(resourceCollector.exportToIpynb())

        expect = {'1': '# code 1\nprint("This is from codePart1.ipynb")',
                  '2': '# code 2\nprint("This is from codePart2.ipynb")'}

        self.assertEqual(2, self.codeResourceContainer.getAnalyseCodeCells().keys().__len__())
        self.assertEqual(expect, self.codeResourceContainer.getAnalyseCodeCells())

    def test_getAnalyseCodeCellsTwoCellSameId(self):
        self.codeResourceContainer.add(self.resourceCollector1.exportToIpynb())

        resourceCollector = ResourceCollector(ResourceType.IPYNB)
        resourceCollector.collectFromLocalFile("./ResourceForTests/codePart3.ipynb")
        self.codeResourceContainer.add(resourceCollector.exportToIpynb())

        expect = {'1': '# code 1\nprint("This is from codePart3.ipynb")'}

        self.assertEqual(1, self.codeResourceContainer.getAnalyseCodeCells().keys().__len__())
        self.assertEqual(expect, self.codeResourceContainer.getAnalyseCodeCells())
