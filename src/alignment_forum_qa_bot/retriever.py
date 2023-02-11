from abc import ABC
import json
import os
from pathlib import Path
from typing import TypedDict, List

from dotenv import load_dotenv

from alignment_forum_qa_bot.get_data import download_posts
from alignment_forum_qa_bot.parse_af_post_json import parse_posts_raw

load_dotenv()


class RetrievedParagraph(TypedDict):
    title: str
    author: str
    paragraph: str


class Retriever(ABC):
    def __init__(self):
        ...

    def retrieve(self, query: str) -> List[RetrievedParagraph]:
        raise NotImplementedError


class StubRetriever(Retriever):
    def retrieve(self, query: str) -> List[RetrievedParagraph]:
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
                "author": "paulchristiano",
                "paragraph": "Capabilities and alignment are basically the same thing!",
            },
        ]


class KeywordSearchRetriever(Retriever):
    def __init__(self):
        data_dir = Path(os.environ["DATA_DIR"])

        if not data_dir.exists():
            download_posts()

        with open(data_dir / "posts.json") as f:
            posts = json.load(f)
        self.paragraphs = parse_posts_raw(posts)

    def retrieve(self, query: str) -> List[RetrievedParagraph]:
        relevant_paragraphs = self.paragraphs[self.paragraphs["paragraph"].apply(lambda x: query in x)]
        return relevant_paragraphs.to_dict(orient="records")


if __name__ == "__main__":
    retriever = KeywordSearchRetriever()
    print(retriever.retrieve("RLHF"))
