from dotenv import dotenv_values
import streamlit as st

from alignment_forum_qa_bot import QABot

# Load API key and initialize Alignment Forum question-answer bot.
config = dotenv_values(".env")
bot = QABot(config["OPENAI_API_KEY"])

st.title("Alignment Forum Summarization Workbench")

query_text = st.text_input("Query keywords", value="")

response = bot.query(query_text)

st.subheader("Query keywords")
st.write(query_text)

st.subheader("Alignment Forum response")
st.write(response)
