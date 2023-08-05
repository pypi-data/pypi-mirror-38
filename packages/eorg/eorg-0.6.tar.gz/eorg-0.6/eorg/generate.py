from io import StringIO
from eorg.const import Token, ESCAPE
from eorg import tokens
from eorg.tokens import Token
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def src(doc, code, cls="", root=True):
    try:
        lexer = get_lexer_by_name(code.attrs.get("language", "shell"))
    except pygments.util.ClassNotFound as e:
        lexer = get_lexer_by_name(code.attrs.get("language", "text"))

    return highlight(code.value, lexer, HtmlFormatter(linenos=True))


def img(doc, item, cls="", root=True):
    caption = doc.previous(tokens.CAPTION)
    text = ""
    if caption:
        text = f'<p class="center-align">{caption.value}</p>'
    return f'<img{cls} style="margin:auto;" src="{item.value[0]}" alt="{item.value[1]}" />{text}'


def link(doc, item, cls="", root=True):
    return f'<a {cls} style="margin:auto;" href="{item.value[0]}">{item.value[1]}</a>'


def parse_list_html(doc, token, cls="", root=True):
    response = StringIO()
    response.write(f"<p{cls}>")

    for item in token.value:
        response.write(handle_token(doc, item, False))
    response.write(f"</p>")
    response.seek(0)
    return response.read()


def parse_text_html(doc, token, cls="", root=True):
    return f"{token.value}"


def blockquote(doc, token, cls="", root=True):
    return "<blockquote%s>%s</blockquote>\n" % (
        cls,
        token.value.replace("\n", "<br />"),
    )


def header(doc, item, cls="", root=True):
    depth = "1"
    if item.attrs:
        depth = item.attrs.get("depth", "1")
    return "<h%s%s>%s</h%s>\n" % (depth, cls, item.value, depth)


builddoc = {
    tokens.HEADER: (header, None),
    tokens.IMAGE: (img, "materialboxed center-align responsive-img"),
    tokens.LINK: (link, None),
    tokens.BOLD: ("b", None),
    tokens.UNDERLINED: ("u", None),
    tokens.ITALIC: ("i", None),
    tokens.VERBATIM: ("code", None),
    tokens.LIST: (parse_list_html, "flow-text"),
    tokens.TEXT: (parse_text_html, "flow-text"),
    tokens.SOURCE: (src, None),
    tokens.EXAMPLE: (blockquote, None),
    tokens.RESULTS: (blockquote, None),
}


def handle_token(doc, item, root=False):
    response = StringIO()
    match = builddoc.get(item.token)

    if not match:
        return ""

    tag, cls = match
    if cls:
        cls = f' class="{cls}"'
    else:
        cls = ""
    if callable(tag):
        return tag(doc, item, cls, root=root)

    else:
        return "<%s%s>%s</%s>\n" % (tag, cls, item.value, tag)


def html(doc):
    response = StringIO()
    for item in doc:
        response.write(handle_token(doc, item, True))
    response.seek(0)
    return response
