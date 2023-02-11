def test_subboilerplate_get_goodbye():
    from boilerplate.subboilerplate import get_goodbye

    assert isinstance(get_goodbye(), str)
