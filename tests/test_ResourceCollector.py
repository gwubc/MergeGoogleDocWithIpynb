import unittest

import nbformat

from MergeGoogleDocWithIpynb.ResourceCollector import ResourceCollector, ResourceType, ResourceUnableCollectException, \
    ResourceExportException


class test_ResourceCollector(unittest.TestCase):

    def test_collectFromLocalFile(self):
        expect = "This is markdown 1\n\n{{ code 1 }}\n\nEnd of markdown1\n".replace("\n", "")

        resourceCollector = ResourceCollector(ResourceType.MARKDOWN)
        resourceCollector.collectFromLocalFile("./ResourceForTests/markdown1.md")
        self.assertEqual(expect, resourceCollector.exportToMd().replace("\n", ""))

        resourceCollector = ResourceCollector(ResourceType.HTML)
        resourceCollector.collectFromLocalFile("./ResourceForTests/markdown1.html")
        self.assertEqual(expect, resourceCollector.exportToMd().replace("\n", ""))

        resourceCollector = ResourceCollector(ResourceType.HTML)
        self.assertRaises(ResourceUnableCollectException, resourceCollector.collectFromLocalFile, "./File/Not/Exist.html")

    def test_collectFromRemoteFile(self):
        expect = "This is markdown 1\n\n{{ code 1 }}\n\nEnd of markdown1\n".replace("\n", "")

        resourceCollector = ResourceCollector(ResourceType.GOOGLEDOC)
        resourceCollector.collectFromRemoteFile("https://docs.google.com/document/d/1VydaTvK2sBTAkG_NkBzXzI5hLG12yjUIUzsHmrW2LDk/edit?usp=sharing")
        self.assertEqual(expect, resourceCollector.exportToMd().replace("\n", ""))

        resourceCollector = ResourceCollector(ResourceType.GOOGLEDOC)
        self.assertRaises(ResourceUnableCollectException, resourceCollector.collectFromRemoteFile,
                          "https://docs.google.com/document/1VydaTvK2sBTAkG_NkBzXzI5hLG12yjUIUzsHmrW2LDk/edit?usp=sharing")

        resourceCollector = ResourceCollector(ResourceType.HTML)
        resourceCollector.collectFromRemoteFile("https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/tests/ResourceForTests/markdown1.html")
        self.assertEqual(expect, resourceCollector.exportToMd().replace("\n", ""))

        resourceCollector = ResourceCollector(ResourceType.MARKDOWN)
        resourceCollector.collectFromRemoteFile("https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/tests/ResourceForTests/markdown1.md")
        self.assertEqual(expect, resourceCollector.exportToMd().replace("\n", ""))

        resourceCollector = ResourceCollector(ResourceType.IPYNB)
        resourceCollector.collectFromRemoteFile("https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/tests/ResourceForTests/codePart1.ipynb")
        nbSource = nbformat.reads(resourceCollector.exportToIpynb(), as_version=4)
        self.assertEqual('# code 1\nprint("This is from codePart1.ipynb")', nbSource.cells[0]['source'])

        resourceCollector = ResourceCollector(ResourceType.HTML)
        self.assertRaises(ResourceUnableCollectException, resourceCollector.collectFromRemoteFile,
                          "https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/tests/ResourceForTests//File/Not/Exist.html")


        resourceCollector = ResourceCollector(ResourceType.UNKNOWN)
        self.assertRaises(ResourceUnableCollectException, resourceCollector.collectFromRemoteFile,
                          "https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/tests/ResourceForTests//File/Not/Exist.html")


    def test_collectTwice(self):
        resourceCollector = ResourceCollector(ResourceType.HTML)
        resourceCollector.collectFromRemoteFile("https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/tests/ResourceForTests/markdown1.html")
        self.assertRaises(ResourceUnableCollectException, resourceCollector.collectFromLocalFile, "./ResourceForTests/markdown1.html")
        self.assertRaises(ResourceUnableCollectException, resourceCollector.collectFromRemoteFile, "./ResourceForTests/markdown1.html")

    def test_failToExport(self):
        resourceCollector = ResourceCollector(ResourceType.MARKDOWN)
        self.assertEqual("", resourceCollector.exportToMd())
        self.assertRaises(ResourceExportException, resourceCollector.exportToIpynb)

        resourceCollector = ResourceCollector(ResourceType.GOOGLEDOC)
        self.assertEqual("", resourceCollector.exportToMd())
        self.assertRaises(ResourceExportException, resourceCollector.exportToIpynb)

        resourceCollector = ResourceCollector(ResourceType.HTML)
        self.assertEqual("", resourceCollector.exportToMd())
        self.assertRaises(ResourceExportException, resourceCollector.exportToIpynb)

        resourceCollector = ResourceCollector(ResourceType.IPYNB)
        self.assertEqual("", resourceCollector.exportToIpynb())
        self.assertRaises(ResourceExportException, resourceCollector.exportToMd)

