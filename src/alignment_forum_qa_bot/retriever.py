from abc import ABC
from typing import TypedDict


class RetrievedParagraph(TypedDict):
    title: str
    author: str
    paragraph: str


class Retriever(ABC):
    def __init__(self):
        ...

    def retrieve(self, query: str) -> list[RetrievedParagraph]:
        raise NotImplementedError


class StubRetriever(Retriever):
    def retrieve(self, query: str) -> list[RetrievedParagraph]:
        return [
            {
                "title": "RLFH IS SHIT",
                "author": "johnswentworth",
                "paragraph": "RLHF will kill us all!",
            },
            {
                "title": "RLFH IS SHIT",
                "author": "johnswentworth",
                "paragraph": "And it's all Paul Christiano's fault.",
            },
            {
                "title": "RLHF IS AMAZING",
                "author": "paulchristiano",
                "paragraph": "RLHF is great!",
            },
            {
                "title": "RLFH IS SHIT",
                "author": "johnswentworth",
                "paragraph": "Capabilities and alignment are basically the same thing!",
            },
        ]
