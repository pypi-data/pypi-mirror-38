from eorg import tokens
ESCAPE = ['\n']


METADATA = ['TITLE', 'AUTHOR', 'EMAIL', 'DESCRIPTION', 'KEYWORDS', 'FILETAGS', 'DATE']
t_META = r"^[#]\+(" + '|'.join(METADATA) +")\:"
t_BLANK_LINE = '^\s*$'
t_COMMENT_BEGIN = r"^\#\+BEGIN_COMMENT"
t_COMMENT_END = r"^\#\+END_COMMENT"
t_EXAMPLE_BEGIN = r"^\#\+BEGIN_EXAMPLE"
t_EXAMPLE_END = r"^\#\+END_EXAMPLE"
t_SRC_BEGIN = r"^\#\+BEGIN_SRC\s+"
t_SRC_END = r"^\#\+END_SRC"
t_RESULTS_START = r"^\#\+RESULTS:"
t_CAPTIONS = r"^\#\+CAPTION:"
t_IMG = r"^\[\[\s]]$"
t_RESULTS_END = r"^\:..*"

t_HEADER = r"^\*+"

# Start regex, End regex, skip start, skip end, count matches
TOKENS = {
    tokens.META: (t_META, False, 2, -1, False),
    tokens.COMMENT: (t_COMMENT_BEGIN, t_COMMENT_END, 2, None, False),
    tokens.EXAMPLE: (t_EXAMPLE_BEGIN, t_EXAMPLE_END, 2, None, False),
    tokens.IMAGE: (t_IMG, False, 2, None, False),
    tokens.CAPTION: (t_CAPTIONS, False, 2, None, False),
    tokens.SOURCE: (t_SRC_BEGIN, t_SRC_END, 2, None, False),
    tokens.RESULTS: (t_SRC_BEGIN, t_SRC_END, 2, None, False),
    tokens.HEADER: (t_HEADER, False, 1, None, True),
}



class Token:
    __slots__ = ["token", "value"]

    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __repr__(self):
        return f"Token(token={self.token}, value={self.value})"

image_extensions = (".jpg", ".jpeg", ".png", ".svg")
