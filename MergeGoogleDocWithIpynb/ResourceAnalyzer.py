from MergeGoogleDocWithIpynb.Types import ResourceType, CodeResource, MarkdownResource


class ResourceAnalyzer:
    resourceType: ResourceType = None
    rawResource: str = None

    def __init__(self, resourceType, resource):
        self.resourceType = resourceType
        self.rawResource = resource

    def analysis(self) -> CodeResource | MarkdownResource:
        pass
