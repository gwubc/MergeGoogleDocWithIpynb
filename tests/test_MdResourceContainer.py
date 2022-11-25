import unittest

from MergeGoogleDocWithIpynb.MdResourceContainer import MdResourceContainer, BlockType
from MergeGoogleDocWithIpynb.ResourceCollector import ResourceCollector, ResourceType


class test_MdResourceContainer(unittest.TestCase):
    mdResourceContainer = None
    resourceCollector1 = None

    def setUp(self) -> None:
        self.mdResourceContainer = MdResourceContainer()
        self.resourceCollector1 = ResourceCollector(ResourceType.MARKDOWN)
        self.resourceCollector1.collectFromLocalFile("./ResourceForTests/markdown1.md")

    def test_addOnce(self):
        self.mdResourceContainer.add(self.resourceCollector1.exportToMd())
        expect = [(BlockType.MD, 'This is markdown 1'), (BlockType.CODE, '1'), (BlockType.MD, 'End of markdown1')]
        self.assertEqual(expect, self.mdResourceContainer.getAnalysedTextBlock())

    def test_addTwice(self):
        self.mdResourceContainer.add(self.resourceCollector1.exportToMd())

        resourceCollector2 = ResourceCollector(ResourceType.MARKDOWN)
        resourceCollector2.collectFromLocalFile("./ResourceForTests/markdown2.md")
        self.mdResourceContainer.add(resourceCollector2.exportToMd())

        expect = [(BlockType.MD, 'This is markdown 1'),
                  (BlockType.CODE, '1'),
                  (BlockType.MD, 'End of markdown1'),
                  (BlockType.NEWBLOCK, ''),
                  (BlockType.MD, 'This is markdown 2'),
                  (BlockType.CODE, '2'),
                  (BlockType.MD, 'End of markdown2')]

        self.assertEqual(expect, self.mdResourceContainer.getAnalysedTextBlock())

    def test_addMdWithComment(self):
        resourceCollector2 = ResourceCollector(ResourceType.MARKDOWN)
        resourceCollector2.collectFromLocalFile("./ResourceForTests/markdown3.md")
        self.mdResourceContainer.add(resourceCollector2.exportToMd())
        self.mdResourceContainer.removeLeadingTrailingBlankLine = False

        expect = [(BlockType.MD, '\n##Some Title\n'), (BlockType.NEWBLOCK, ''), (BlockType.MD, '\nMore text\n\n\nLast word.')]
        self.assertEqual(expect, self.mdResourceContainer.getAnalysedTextBlock())


    def test_add(self):
        testBlock = [(BlockType.OTHER, "")]

        expect = []
        self.assertEqual(expect, self.mdResourceContainer._mergeTextBlock(testBlock))
