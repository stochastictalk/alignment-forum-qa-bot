from typing import List

import openai

from .retriever import StubRetriever
from .retriever import RetrievedParagraph


class QABot:
    def __init__(self, openai_api_key: str = None):
        """
        Parameters
        ----------
        openai_api_key : str
            OpenAI API key.
        """
        if openai_api_key is None:
            openai.api_key = "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"

        self._post_retriever = StubRetriever()

    def query(self, query_text: str) -> str:
        """Asks a question about alignment forum's post corpus using OpenAI's completion API.

        Parameters
        ----------
        text : str
            The query input by the Alignment Forum user.
        """
        posts = self._post_retriever.retrieve(query=query_text)
        prompt = self._get_prompt(query_text, posts)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.8,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"],
        )
        return response

    def _get_prompt(self, query_text: str, posts: List[RetrievedParagraph]):
        """Maps posts and question to prompt."""
        return "Prompt pending! @TODO"
