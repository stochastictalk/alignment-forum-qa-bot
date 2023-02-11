from pytest import raises


def test_hello_world():
    from alignment_forum_qa_bot import get_hello

    assert isinstance(get_hello(), str)

    with raises(TypeError):
        get_hello("Angela", "Augustus")
