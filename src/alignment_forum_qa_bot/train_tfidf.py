import os
from pathlib import Path
import pickle

from sklearn import feature_extraction

from alignment_forum_qa_bot.normalizer import Normalizer
from alignment_forum_qa_bot.parse_af_post_json import parse_posts_raw


def bow_fit(corpus_raw, max_features=10000, ngram_range=(1, 2)):
    normalizer = Normalizer()
    corpus = normalizer(corpus_raw)
    tfidf_vectorizer = feature_extraction.text.TfidfVectorizer(max_features=max_features, ngram_range=ngram_range)
    tfidf_vectorizer.fit(corpus["paragraph_processed"])
    return tfidf_vectorizer


def main():
    save_path = Path(os.environ["DATA_DIR"]) / "tfidf_vectorizer.pkl"

    corpus_raw = parse_posts_raw()
    tfidf_vectorizer = bow_fit(corpus_raw)
    with save_path.open("wb") as f:
        pickle.dump(tfidf_vectorizer, f)


if __name__ == "__main__":
    main()
