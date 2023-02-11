import openai


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

    def query(text: str) -> str:
        """Asks a question about alignment forum's post corpus using OpenAI's completion API."""
        prompt = text
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
