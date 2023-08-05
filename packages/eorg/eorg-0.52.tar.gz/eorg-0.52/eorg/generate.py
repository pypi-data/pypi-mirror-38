from io import StringIO
from eorg.const import Token, ESCAPE
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
    caption = doc.previous("CAPTION")
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
    # if its the start of a text body wrap html tags
    # else more complicated so return the tags
    # if root is True:
    #    return f"<p{cls}>{token.value}</p>"
    return f"{token.value}"


def blockquote(doc, token, cls="", root=True):
    return "<blockquote%s>%s</blockquote>\n" % (
        cls, token.value.replace("\n", "<br />")
    )


builddoc = {
    "HEADER1": ("h2", None),
    "HEADER2": ("h3", None),
    "HEADER3": ("h4", None),
    "IMG": (img, "materialboxed center-align responsive-img"),
    "LINK": (link, None),
    "B": ("b", None),
    "U": ("u", None),
    "I": ("i", None),
    "V": ("code", None),
    "LIST": (parse_list_html, "flow-text"),
    "TEXT": (parse_text_html, "flow-text"),
    "SRC_BEGIN": (src, None),
    "EXAMPLE": (blockquote, None),
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
