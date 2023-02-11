from dotenv import dotenv_values
import streamlit as st

from alignment_forum_qa_bot import QABot


@st.cache_resource
def get_qa_bot():
    # Load API key and initialize Alignment Forum question-answer bot.
    config = dotenv_values(".env")
    bot = QABot(config["OPENAI_API_KEY"])
    return bot


bot = get_qa_bot()

st.title("Alignment Forum Opinion Summarizer")

query_text = st.text_input("Alignment approach", key="query_text")

if "query_text" in st.session_state:
    response = bot.query(st.session_state["query_text"], method="summarize-by-author")

    st.subheader("Alignment approach")
    st.write(query_text)

    st.subheader("Alignment Forum response")
    st.write(response)
