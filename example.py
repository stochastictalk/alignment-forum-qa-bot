from dotenv import dotenv_values

from alignment_forum_qa_bot import QABot

config = dotenv_values(".env")
bot = QABot(config["OPENAI_API_KEY"])
response = bot.query("cyborg")
print(response)
