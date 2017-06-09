"""
Convert Markdown into HTML.
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
    Inserts list tags appropriately into corpus.

    Parameters
    ----------
    corpus : str
        The raw or partially converted Markdown text.

    Returns
    -------
    ol_ul_finished : str
        The corpus after list tags are inserted.

    >>> ul_test = '- i1\n+ i2\n* i3'
    >>> lists(ul_test)
    '<ul><li>i1</li>\n<li>i2</li>\n<li>i3</li></ul>'
    >>> ul_test = '2. i1\n69. i2\n1337. i3'
    >>> lists(ul_test)
    '<ol><li>i1</li>\n<li>i2</li>\n<li>i3</li></ol>'
    >>> mixed_test = '- P1\n78. P2\n* P3'
    >>> lists(mixed_test)
    '<ul><li>P1</li></ul>\n\n<ol><li>P2</li></ol>\n\n<ul><li>P3</li></ul>'
    """
# wrap each unordered item in its own list
    ul_wrapped = re.sub(r'(-|\+|\*) (.*)', r'<ul><li>\g<2></li></ul>', corpus)
# wrap each ordered item in its own list
    ol_ul_wrapped = re.sub(r'(\d+\.) (.*)', r'<ol><li>\g<2></li></ol>', ul_wrapped)

# separate unordered and ordered lists
    separated = re.sub(r'</ul>\n(.*)<ol>', r'</ul>\n\n\g<1><ol>', ol_ul_wrapped)
    separated = re.sub(r'</ol>\n(.*)<ul>', r'</ol>\n\n\g<1><ul>', separated)

# remove back-to-back </ul><ul>
    ul_finished = re.sub(r'</ul>\n(.*)<ul>', '\n', separated)
# remove back-to-back </ul><ul>
    ol_ul_finished = re.sub(r'</ol>\n(.*)<ol>', '\n', ul_finished)
    return ol_ul_finished


def italics(corpus):
    r"""
    Italicizes words in the markdown that are surrounded by
    single asterisks.

    Parameters
    ----------
    corpus : str
        The raw or partially converted Markdown text.

    Returns
    -------
    str
        The `corpus` with <em> tags inserted.

    >>> text = '*italic*'
    >>> italics(text)
    '<em>italic</em>'
    """
    return re.sub(r'\*([^\n]+)\*', r'<em>\g<1></em>', corpus)


def bold(corpus):
    r"""
    Bolds words in the markdown that are surrounded by
    double asterisks.

    Parameters
    ----------
    corpus : str
        The raw or partially converted Markdown text.

    Returns
    -------
    str
        The `corpus` with <strong> tags inserted.

    >>> text = '**bold**'
    >>> bold(text)
    '<strong>bold</strong>'
    """
    return re.sub(r'\*\*([^\n]+)\*\*', r'<strong>\g<1></strong>', corpus)


def headers(corpus):
    r"""
    Places headers up to h6 into the corpus.

    Parameters
    ----------
    corpus : str
        Markdown string to convert.

    Returns
    -------
        A string of HTML converted from the `corpus`.

    >>> headers('#hello')
    '#hello'
    >>> headers('# hello')
    '<h1>hello</h1>'
    >>> headers('## hello')
    '<h2>hello</h2>'
    >>> headers('###  \t hello')
    '<h3>hello</h3>'
    >>> headers('####\thello')
    '<h4>hello</h4>'
    >>> headers('#####\t   hello')
    '<h5>hello</h5>'
    >>> headers('######    hello')
    '<h6>hello</h6>'
    >>> headers('#######\t hello')
    '#######\t hello'
    """
    for i in range(6, 0, -1):
        corpus = re.sub(r'(^|\n)'+f'({"#"*i})'+'[ \t]+([^\n]+)',
                        fr'\g<1><h{i}>\g<3></h{i}>', corpus)
    return corpus


def html(corpus):
    r"""
    Converts raw Markdown into HTML.

    Parameters
    ----------
    corpus : str
        The raw Markdown.

    Returns
    -------
    converted_text : str
        Resulting HTML from converting `corpus`.

    >>> text = 'P1\n\nP2\n- 1\n- 2\nP2\n\nP3'
    >>> html(text)
    '<article><p>P1</p>\n<p>P2\n<ul><li>1</li>\n<li>2</li></ul>\nP2</p>\n<p>P3</p></article>'
    >>> bolditalic = '***hello***'
    >>> html(bolditalic)
    '<article><p><strong><em>hello</em></strong></p></article>'
    """
    text = paragraphs(lists(italics(bold(headers(corpus)))))
    return f'<article>{text}</article>'


def run():
    """
    Command line tool to convert Markdown file into HTML.
    """
    import argparse
    parser = argparse.ArgumentParser(description='Convert Markdown into HTML.')
    parser.add_argument('markdown_file')
    args = parser.parse_args()
    with open(args.markdown_file, 'r') as file_obj:
        markdown = file_obj.read().rstrip('\n')
    print(html(markdown))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    run()
