import ply.lex as lex

reserved = {
    "block" : "BLOCK",
    "add" : "ADD",
    "print" : "PRINT",
    "view" : "VIEW",
    "mine" : "MINE",
    "export" : "EXPORT",
    "str" : "STR",
    "int" : "INT",
    "long" : "LONG",
    "float" : "FLOAT",
    "List" : "LIST",
    "Tuple" : "TUPLE",
    "Dict" : "DICT"
}

tokens = (
    "ID",
    "BLOCK",
    "ADD",
    "PRINT",
    "VIEW",
    "MINE",
    "EXPORT",
    "STR",
    "FLOAT",
    "INT",
    "LONG",
    "LIST",
    "TUPLE",
    "DICT",
    "NUM",
    "ASSIGN",
    "TYPEASSIGN", 
    "SEPARATOR",
    "LPAREN",
    "RPAREN",
    "COMMENT",
    "FLOATVAL",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
)

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, "ID")
    return t
def t_FLOATVAL(t):
    r'\d+\.\d+'           # Match something like 3.14 or 42.0
    t.value = float(t.value)
    return t
def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t
t_ASSIGN = r'='
t_TYPEASSIGN = r':'
t_SEPARATOR = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ignore = ' \t'  # Ignore whitespaces
def t_ignore_newline(t):
    r'(\r\n|\r|\n)+'
    t.lexer.lineno += len(t.value.replace('\r', ''))
def t_COMMENT(t):
    r'//.*'
    pass
def t_STR(t):
    r'"[^"]*"'            # Match any text between quotes
    t.value = t.value[1:-1]  # Strip quotes
    return t
def t_error(t):  # Error handler for illegal characters
    print(f"[Lexical Error] Line {t.lineno}: Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

my_lexer = lex.lex()