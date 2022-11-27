from enum import Enum
from typing import List


class BlockType(Enum):
    CODE = 1
    MD = 2
    NEWBLOCK = 3
    OTHER = 4


CodeResource = dict[str, str]
MarkdownResource = List[tuple[BlockType, str]]


class ResourceType(Enum):
    MARKDOWN = 1
    HTML = 2
    IPYNB = 3
    GOOGLEDOC = 4

    UNKNOWN = 10
