import os.path
import re
from enum import Enum

from markdownify import markdownify as md

import requests


class ResourceUnableCollectException(Exception):
    pass


class ResourceExportException(Exception):
    pass


class ResourceType(Enum):
    MARKDOWN = 1
    HTML = 2
    IPYNB = 3
    GOOGLEDOC = 4

    UNKNOWN = 10


class ResourceCollector:
    resourceType: ResourceType = None
    _used = False
    _data = None

    def __init__(self, type: ResourceType):
        self.resourceType = type
        self._data = ""
        self._used = False

    def _download(self, url) -> str:
        html = requests.get(url)
        if html.status_code != 200:
            raise ResourceUnableCollectException(f"{url} not reachable. Status code: {html.status_code}")
        html.encoding = "utf8"
        return html.text

    def collectFromLocalFile(self, path) -> str:
        if self._used:
            raise ResourceUnableCollectException("ResourceCollector Should Not be reused")
        if not os.path.exists(path):
            raise ResourceUnableCollectException(f"{path}. Not exists")

        with open(path, encoding="utf8") as f:
            self._data = f.read()

        self._used = True
        return self.__str__()

    def collectFromRemoteFile(self, url) -> str:
        if self._used:
            raise ResourceUnableCollectException("ResourceCollector Should Not be reused")

        match self.resourceType:
            case ResourceType.GOOGLEDOC:
                docHtml = self._GoogleDocToHtml(self._getDocIdFromGoogleLink(url))
                docHtml = re.sub("<style.*</style>", '', docHtml)
                self._data = docHtml

            case ResourceType.HTML | ResourceType.MARKDOWN:
                self._data = self._download(url)

            case ResourceType.IPYNB:
                self._data = self._download(url)

            case _:
                raise ResourceUnableCollectException("Unknown ResourceType")

        self._used = True
        return self.__str__()

    def _htmlToMd(self, htmlTxt) -> str:
        return md(htmlTxt)

    def _GoogleDocToHtml(self, id) -> str:
        htmlTxt = self._download(
            f"https://docs.google.com/feeds/download/documents/export/Export?id={id}&exportFormat=html")
        return htmlTxt

    def _getDocIdFromGoogleLink(self, url: str) -> str:
        components = url.split("/")
        for i in range(len(components)):
            if components[i] == 'd':
                return components[i + 1]
        raise ResourceUnableCollectException(f"Cannot find doc id: {url}")

    def exportToMd(self) -> str:
        match self.resourceType:
            case ResourceType.GOOGLEDOC | ResourceType.HTML:
                return self._htmlToMd(self._data)
            case ResourceType.MARKDOWN:
                return self._data
            case _:
                raise ResourceExportException(
                    "Unable export as markdown. Only google doc, html and markdown can be export as markdown")

    def exportToIpynb(self) -> str:
        match self.resourceType:
            case ResourceType.IPYNB:
                return self._data

            case _:
                raise ResourceExportException("Unable export as markdown. Only ipynb can be export as ipynb")

    def __str__(self):
        return self._data
