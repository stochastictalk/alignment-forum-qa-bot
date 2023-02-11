def get_goodbye(name: str = None):
    """Says goodbye!

    Parameters
    ----------
    name : str
        The name to say ciao to.

    Returns
    -------
    str
        Goodbye!
    """

    return f"Goodbye, {name if name is not None else 'world'}!"
