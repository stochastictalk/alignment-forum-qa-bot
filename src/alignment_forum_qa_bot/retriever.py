from abc import ABC
from pathlib import Path
import pickle
from typing import TypedDict, List
import os

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv


from alignment_forum_qa_bot.normalizer import Normalizer
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

        self.paragraphs = parse_posts_raw()

    def retrieve(self, query: str) -> List[RetrievedParagraph]:
        relevant_paragraphs = self.paragraphs[self.paragraphs["paragraph"].apply(lambda x: query in x)]
        return relevant_paragraphs.to_dict(orient="records")


class TFIDFRetreiver(Retriever):
    def __init__(self, threshold=0.8):
        self.raw_paragraphs = parse_posts_raw()
        self.normalizer = Normalizer()
        self.tfidf_vectorizer = self.load_tfidf_vectorizer()
        self.normalized_paragraphs = self.load_normalized_paragraphs()
        self.corpus_vectors = self.bow_transform(self.normalized_paragraphs)
        self.threshold = threshold

    def retrieve(self, query: str) -> List[RetrievedParagraph]:
        query = self.normalizer.norm_sent(query)
        query_vector = self.tfidf_vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.corpus_vectors).flatten()
        should_keep = scores > self.threshold
        return self.raw_paragraphs[should_keep].to_dict(orient="records")

    def bow_transform(self, data):
        return self.tfidf_vectorizer.transform(data["paragraph_processed"])

    def load_tfidf_vectorizer(self):
        path = Path(os.environ["DATA_DIR"]) / "tfidf_vectorizer.pkl"
        with path.open("rb") as f:
            return pickle.load(f)

    def load_normalized_paragraphs(self):
        path = Path(os.environ["DATA_DIR"]) / "normalized_paragraphs.parquet"
        return pd.read_parquet(path)


if __name__ == "__main__":
    retriever = TFIDFRetreiver(threshold=0.5)
    print(retriever.retrieve("RLHF"))
