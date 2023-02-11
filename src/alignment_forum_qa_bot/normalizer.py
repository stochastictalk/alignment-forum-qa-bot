import os
from pathlib import Path
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tqdm import tqdm

from alignment_forum_qa_bot.parse_af_post_json import parse_posts_raw


class Normalizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = stopwords.words()

    # normalization of question sentences
    def norm_sent(self, sent, rm_stopwords=False, stemming=True, lemmatization=False):
        # tokenize - sentence to word
        words = word_tokenize(sent)

        # take if all characters in the string are alphabets and then decapitalize
        sent = [w.lower() for w in words if w.isalpha()]

        # remove stopwords
        if rm_stopwords:
            sent = [w for w in sent if w not in self.stopwords]

        # apply lemmatization
        if lemmatization:
            sent = [self.lemmatizer.lemmatize(w, pos="n") for w in sent]
            sent = [self.lemmatizer.lemmatize(w, pos="v") for w in sent]
            sent = [self.lemmatizer.lemmatize(w, pos=("a")) for w in sent]

        # apply stemming
        if stemming:
            sent = [self.stemmer.stem(w) for w in sent]

        sent = " ".join(sent)
        return sent

    def __call__(self, data):
        result = []
        for paragraph in tqdm(data["paragraph"]):
            result.append(self.norm_sent(paragraph, rm_stopwords=True, lemmatization=True, stemming=True))
        data["paragraph_processed"] = result
        return data


if __name__ == "__main__":
    raw_paragraphs = parse_posts_raw()
    normalizer = Normalizer()
    normalized_paragraphs = normalizer(raw_paragraphs)
    save_path = Path(os.environ["DATA_DIR"]) / "normalized_paragraphs.parquet"
    normalized_paragraphs.to_parquet(save_path)
