from typing import TypedDict
import pandas as pd


class RawData(TypedDict):
    title: str
    author: str
    htmlBody: str


def parse_raw_data(raw_data: list[RawData]):
    titles = []
    authors = []
    paragraphs = []
    for post in raw_data:
        titles.append(post["title"])
        authors.append(post["author"])
        paragraphs.append(post["htmlBody"])
    result = pd.DataFrame({"title": titles, "author": authors, "paragraph": paragraphs})
    result = result[result.paragraph.notna()]
    return result
