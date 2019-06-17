def fill_none_if_empty(d: dict) -> dict:
    """値が空文字の場合にNoneへ変更する

    :param d: 辞書
    :return: 変更後の辞書

    Usage:

        >>> fill_none_if_empty({"a": 1, "b": "", "c": 0, "d": None})
        {'a': 1, 'b': None, 'c': 0, 'd': None}
    """
    return {k: v if v != "" else None for k, v in d.items()}
