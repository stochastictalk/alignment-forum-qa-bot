def get_hello(name: str = None):
    """Says hello!

    Parameters
    ----------
    name : str
        The name to say howdy to.

    Returns
    -------
    str
        Hello!
    """

    return f"Hello, {name if name is not None else 'world'}!"
