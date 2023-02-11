def test_subalignment_forum_qa_bot_get_goodbye():
    from alignment_forum_qa_bot.subalignment_forum_qa_bot import get_goodbye

    assert isinstance(get_goodbye(), str)
