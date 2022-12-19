from MergeGoogleDocWithIpynb.MergeToIpynb import MergeToIpynb
from MergeGoogleDocWithIpynb.CodeResourceContainer import CodeResourceContainer
from MergeGoogleDocWithIpynb.MdResourceContainer import MdResourceContainer
from MergeGoogleDocWithIpynb.ResourceCollector import ResourceCollector
from MergeGoogleDocWithIpynb.Types import ResourceType

code1 = 'https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/Example/ResourceForExample/codePart1.ipynb'
code2 = 'https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/Example/ResourceForExample/codePart2.ipynb'
markdown1 = "https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/Example/ResourceForExample/markdown1.md"
markdown2 = "https://raw.githubusercontent.com/gwubc/MergeGoogleDocWithIpynb/master/Example/ResourceForExample/markdown2.md"
outPath = "./ExampleOut.ipynb"

mdResourceCollector1 = ResourceCollector(ResourceType.MARKDOWN)
mdResourceCollector1.collectFromRemoteFile(markdown1)

mdResourceCollector2 = ResourceCollector(ResourceType.MARKDOWN)
mdResourceCollector2.collectFromRemoteFile(markdown2)

mdResourceContainer = MdResourceContainer()
mdResourceContainer.add(mdResourceCollector1.exportToMarkdownResource())
mdResourceContainer.add(mdResourceCollector2.exportToMarkdownResource())


codeResourceCollector1 = ResourceCollector(ResourceType.IPYNB)
codeResourceCollector1.collectFromRemoteFile(code1)

codeResourceCollector2 = ResourceCollector(ResourceType.IPYNB)
codeResourceCollector2.collectFromRemoteFile(code2)

codeResourceContainer = CodeResourceContainer()
codeResourceContainer.codeBlockRemoveCellId = True
codeResourceContainer.add(codeResourceCollector1.exportToIpynb())
codeResourceContainer.add(codeResourceCollector2.exportToIpynb())


mergeToIpynb = MergeToIpynb(mdResourceContainer, codeResourceContainer)

out = mergeToIpynb.generate(outPath)