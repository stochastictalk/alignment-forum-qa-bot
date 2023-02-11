from pathlib import Path
import json
import pandas as pd
from bs4 import BeautifulSoup
from multiprocessing import Pool
import unicodedata
from typing import Any
from dotenv import load_dotenv
import os

load_dotenv()


def html_to_paragraphs(html_str: str) -> str:
    soup = BeautifulSoup(html_str, features="html.parser")
    texts = []
    for para in soup.find_all("p"):
        text = unicodedata.normalize("NFKD", para.text)
        texts.append(text)
    return texts


def read_posts_json() -> list[dict[str, Any]]:
    data_dir = Path(os.environ["DATA_DIR"])
    with (data_dir / "posts.json").open("r") as f:
        comments_raw = json.load(f)
    return comments_raw


def parse_posts_raw() -> pd.DataFrame:
    """Opens the raw retrieved Alignment Forum comments and parses them.
    Returns a data frame with author, title, paragraph columns. For each
    paragraph that passes the filtering.

    Returns:
        pd.DataFrame: Parsed paragraphs table
    """

    MIN_LEN_PARAGRAPH = 50
    posts_raw = read_posts_json()
    posts_raw = pd.DataFrame(posts_raw)
    comments_raw_mask = ~posts_raw.user.isna()
    comments_raw_mask &= ~posts_raw.htmlBody.isna()
    comments_raw_mask &= posts_raw.htmlBody != ""
    posts_raw = posts_raw.loc[comments_raw_mask]

    posts_raw["author"] = posts_raw.user.apply(lambda e: e["username"])
    posts_raw = posts_raw.drop(columns="user")
    with Pool() as p:
        bodies = p.map(html_to_paragraphs, posts_raw["htmlBody"].to_list())
    posts_raw["paragraph"] = bodies
    posts_raw["n_paragraphs"] = posts_raw["paragraph"].apply(len)
    posts_raw = posts_raw.explode(column="paragraph", ignore_index=True)
    posts_raw = posts_raw.dropna()  # drops a handful of empty paragraphs
    posts_raw["len_paragraph"] = posts_raw["paragraph"].apply(len)
    # for MIN_LEN_PARAGRAPH = 50 this takes out about a third of the paragraphs,
    # which are probably too short to hold relevant information
    posts = posts_raw.loc[
        posts_raw["len_paragraph"] > MIN_LEN_PARAGRAPH,
        ["author", "title", "paragraph"],
    ]
    return posts
