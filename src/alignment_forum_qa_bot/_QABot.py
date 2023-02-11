from typing import List

import openai

from .retriever import KeywordSearchRetriever
from .retriever import RetrievedParagraph


class QABot:
    def __init__(self, openai_api_key: str = None):
        """
        Parameters
        ----------
        openai_api_key : str
            OpenAI API key.
        """
        openai.api_key = openai_api_key
        self._post_retriever = KeywordSearchRetriever()

    def query(self, query_text: str) -> str:
        """Asks a question about alignment forum's post corpus using OpenAI's completion API.

        Parameters
        ----------
        text : str
            The query input by the Alignment Forum user.
        """
        posts = self._post_retriever.retrieve(query=query_text)
        return self._get_response(query_text, posts)

    def _get_response(self, query_text: str, posts: List[RetrievedParagraph], method="summarize-first"):
        case_switch = {"summarize-first": self._summarize_first}

        return case_switch[method](query_text, posts)

    def _summarize_first(self, query_text: str, posts: RetrievedParagraph):
        """Maps posts and question to prompt."""

        try:
            prompt = f"""
            Summarize the following text in less than 200 words.

            {posts[0]["paragraph"]}
            """
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                # temperature=0.8,
                max_tokens=2000,
                # top_p=1,
                # frequency_penalty=0,
                # presence_penalty=0,
                # stop=["\n"],
            )
            return response["choices"][0]["text"]
        except IndexError:
            return f"No posts were found that mention the term '{query_text}'."
