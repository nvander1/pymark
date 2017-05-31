"""
This module is a standalone script to convert Markdown into HTML.
It reads Markdown from stdin and writes HTML to stdout.
"""


import re


def paragraphs(corpus):
    r"""
    Inserts <p> and </p> tags appropriately into corpus.

    Parameters
    ----------
    corpus : str
        The raw or partially converted Markdown text.

    Returns
    -------
    all_paras_added : str
        The corpus after paragraph tags are inserted.

    >>> text = 'P1\n\nP2\nP2\n    \t   \n\n\n  \t\nP3'
    >>> paragraphs(text)
    '<p>P1</p>\n<p>P2\nP2</p>\n<p>P3</p>'
    """
    inner_paras_added = re.sub(r'\n\s*\n', '</p>\n<p>', corpus)
    all_paras_added = f'<p>{inner_paras_added}</p>'
    return all_paras_added


def lists(corpus):
    r"""
    Inserts unorded list tags appropriately into corpus.

    Parameters
    ----------
    corpus : str
        The raw or partially converted Markdown text.

    Returns
    -------
    all_lists_added : str
        The corpus after list tags are inserted.

    >>> text = '- i1\n- i2\n- i3'
    >>> lists(text)
    '<ul><li>i1</li>\n<li>i2</li>\n<li>i3</li></ul>'
    """
# wrap each item in own list
    wrap = re.sub(r'- (.*)', '<ul><li>\g<1></li></ul>', corpus)
# remove back-to-back </ul><ul>
    all_lists_added = re.sub(r'</ul>\n(.*)<ul>', '\n', wrap)
    return all_lists_added


if __name__ == '__main__':
    import doctest
    doctest.testmod()
