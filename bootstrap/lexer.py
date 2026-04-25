from .utils import MeowError

# Token types
TOKEN_KEYWORD = 'KEYWORD'
TOKEN_IDENTIFIER = 'IDENTIFIER'
TOKEN_NUMBER = 'NUMBER'
TOKEN_STRING = 'STRING'
TOKEN_STRING_INTERP = 'STRING_INTERP'
TOKEN_INDENT = 'INDENT'
TOKEN_DEDENT = 'DEDENT'
TOKEN_NEWLINE = 'NEWLINE'
TOKEN_EOF = 'EOF'

TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_STAR = 'STAR'
TOKEN_SLASH = 'SLASH'
TOKEN_DOUBLE_SLASH = 'DOUBLE_SLASH'
TOKEN_PERCENT = 'PERCENT'
TOKEN_DOUBLE_STAR = 'DOUBLE_STAR'

TOKEN_EQ = 'EQ'
TOKEN_EQEQ = 'EQEQ'
TOKEN_BANG = 'BANG'
TOKEN_BANGEQ = 'BANGEQ'
TOKEN_LT = 'LT'
TOKEN_GT = 'GT'
TOKEN_LTE = 'LTE'
TOKEN_GTE = 'GTE'

TOKEN_AND_AND = 'AND_AND'
TOKEN_PLUS_PLUS = 'PLUS_PLUS'
TOKEN_MINUS_MINUS = 'MINUS_MINUS'
TOKEN_MINUS_SLASH = 'MINUS_SLASH'

TOKEN_PLUS_EQ = 'PLUS_EQ'
TOKEN_MINUS_EQ = 'MINUS_EQ'
TOKEN_STAR_EQ = 'STAR_EQ'
TOKEN_SLASH_EQ = 'SLASH_EQ'

TOKEN_COLON = 'COLON'
TOKEN_COMMA = 'COMMA'
TOKEN_DOT = 'DOT'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'
TOKEN_LBRACKET = 'LBRACKET'
TOKEN_RBRACKET = 'RBRACKET'
TOKEN_LBRACE = 'LBRACE'
TOKEN_RBRACE = 'RBRACE'
TOKEN_AT = 'AT'
TOKEN_PIPE = 'PIPE'
TOKEN_ARROW = 'ARROW'

KEYWORDS = {
    'if', 'elif', 'else', 'for', 'while', 'break', 'continue',
    'def', 'return', 'class', 'extends', 'implements', 'init', 'self',
    'try', 'except', 'finally', 'raise', 'error',
    'import', 'from', 'as',
    'true', 'false', 'null', 'fn', 'not', 'in', 'and', 'or',
    'match', 'when',
}

_CHINESE_PUNCT_MAP = {
    '\uff0c': ',',
    '\uff1a': ':',
    '\uff08': '(',
    '\uff09': ')',
    '\u3010': '[',
    '\u3011': ']',
    '\u201c': '"',
    '\u201d': '"',
    '\u2018': "'",
    '\u2019': "'",
    '\uff01': '!',
    '\uff1e': '>',
    '\uff1c': '<',
    '\uff1d': '=',
    '\uff0b': '+',
    '\uff0d': '-',
    '\uff0a': '*',
    '\uff0f': '/',
    '\uff05': '%',
    '\uff20': '@',
    '\uff5c': '|',
}

_CHINESE_OPEN_PUNCT = {'\uff08', '\u3010'}
_CHINESE_CLOSE_PUNCT = {'\uff09', '\u3011'}


class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value!r}, L{self.line}:{self.column})'


class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    def error(self, message):
        raise MeowError(message, self.line, self.column)

    def peek(self, offset=0):
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return '\0'

    def advance(self):
        ch = self.peek()
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def skip_whitespace(self):
        while self.peek() in ' \t\r':
            self.advance()

    def read_string(self):
        quote = self.advance()
        start_line = self.line
        start_col = self.column
        result = []
        while self.peek() != quote:
            if self.peek() == '\0':
                self.error(f"未闭合的字符串，缺少 {quote}")
            if self.peek() == '\\':
                self.advance()
                ch = self.advance()
                escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                result.append(escape_map.get(ch, ch))
            elif self.peek() == '\n':
                self.error("字符串不能跨行")
            else:
                result.append(self.advance())
        self.advance()
        return ''.join(result)

    def read_interp_string(self):
        quote = self.advance()
        start_line = self.line
        start_col = self.column
        parts = []
        current = []
        while self.peek() != quote:
            if self.peek() == '\0':
                self.error(f"未闭合的插值字符串，缺少 {quote}")
            if self.peek() == '\\':
                self.advance()
                ch = self.advance()
                escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                current.append(escape_map.get(ch, ch))
            elif self.peek() == '$' and self.peek(1) == '{':
                if current:
                    parts.append(('str', ''.join(current)))
                    current = []
                self.advance()
                self.advance()
                expr = []
                depth = 1
                while depth > 0 and self.peek() not in ('\0', '\n'):
                    if self.peek() == '{':
                        depth += 1
                    elif self.peek() == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    expr.append(self.advance())
                if self.peek() != '}':
                    self.error("插值表达式未闭合")
                self.advance()
                parts.append(('interp_expr', ''.join(expr)))
            elif self.peek() == '$':
                if current:
                    parts.append(('str', ''.join(current)))
                    current = []
                self.advance()
                var_name = []
                while self.peek().isalnum() or self.peek() == '_':
                    var_name.append(self.advance())
                if not var_name:
                    self.error("插值变量名不能为空")
                parts.append(('interp_var', ''.join(var_name)))
            elif self.peek() == '\n':
                self.error("字符串不能跨行")
            else:
                current.append(self.advance())
        self.advance()
        if current:
            parts.append(('str', ''.join(current)))
        return parts

    def read_number(self):
        num_str = []
        has_dot = False
        has_e = False
        if self.peek() == '0':
            num_str.append(self.advance())
            if self.peek() in ('x', 'X'):
                num_str.append(self.advance())
                while self.peek() in '0123456789abcdefABCDEF':
                    num_str.append(self.advance())
                return int(''.join(num_str), 16)
            if self.peek() in ('b', 'B'):
                num_str.append(self.advance())
                while self.peek() in '01':
                    num_str.append(self.advance())
                return int(''.join(num_str), 2)
        while self.peek().isdigit() or (self.peek() == '.' and not has_dot) or (self.peek() in ('e', 'E') and not has_e):
            if self.peek() == '.':
                has_dot = True
            elif self.peek() in ('e', 'E'):
                has_e = True
                num_str.append(self.advance())
                if self.peek() in ('+', '-'):
                    num_str.append(self.advance())
                continue
            num_str.append(self.advance())
        return float(''.join(num_str)) if has_dot or has_e else int(''.join(num_str))

    def read_identifier(self):
        ident = []
        while self.peek().isalnum() or self.peek() == '_':
            ident.append(self.advance())
        return ''.join(ident)

    def tokenize(self):
        tokens = []
        indent_stack = [0]
        pending_dedents = 0
        at_line_start = True

        while self.pos < len(self.source):
            if not at_line_start:
                self.skip_whitespace()
            ch = self.peek()
            line_number = self.line
            col = self.column

            if ch == '\0':
                break

            if ch == '\n':
                self.advance()
                at_line_start = True
                tokens.append(Token(TOKEN_NEWLINE, None, line_number, col))
                continue

            if ch == '#':
                while self.peek() not in ('\n', '\0'):
                    self.advance()
                continue

            if at_line_start and ch != '\n':
                at_line_start = False
                indent = 0
                while self.peek() == ' ':
                    indent += 1
                    self.advance()
                if self.peek() == '\n' or self.peek() == '#':
                    continue
                if indent > indent_stack[-1]:
                    indent_stack.append(indent)
                    tokens.append(Token(TOKEN_INDENT, None, line_number, col))
                elif indent < indent_stack[-1]:
                    while indent < indent_stack[-1]:
                        indent_stack.pop()
                        tokens.append(Token(TOKEN_DEDENT, None, line_number, col))
                    if indent != indent_stack[-1]:
                        self.error(f"缩进层级不匹配，期望 {indent_stack[-1]} 空格，实际 {indent} 空格")
                ch = self.peek()

            if ch == '"' or ch == "'":
                if self.peek(1) == ch and self.peek(2) == ch:
                    self.advance()
                    self.advance()
                    self.advance()
                    result = []
                    while not (self.peek() == ch and self.peek(1) == ch and self.peek(2) == ch):
                        if self.peek() == '\0':
                            self.error("未闭合的三引号字符串")
                        if self.peek() == '\\':
                            self.advance()
                            esc = self.advance()
                            escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                            result.append(escape_map.get(esc, esc))
                        else:
                            result.append(self.advance())
                    self.advance()
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_STRING, ''.join(result), line_number, col))
                else:
                    str_val = self.read_string()
                    tokens.append(Token(TOKEN_STRING, str_val, line_number, col))
                continue

            if ch == '$' and (self.peek(1) == '"' or self.peek(1) == "'"):
                self.advance()
                quote = self.peek()
                parts = self.read_interp_string()
                tokens.append(Token(TOKEN_STRING_INTERP, parts, line_number, col))
                continue

            if ch.isdigit():
                num = self.read_number()
                tokens.append(Token(TOKEN_NUMBER, num, line_number, col))
                continue

            if ch.isalpha() or ch == '_':
                ident = self.read_identifier()
                if ident in KEYWORDS:
                    tokens.append(Token(TOKEN_KEYWORD, ident, line_number, col))
                else:
                    tokens.append(Token(TOKEN_IDENTIFIER, ident, line_number, col))
                continue

            mapped = _CHINESE_PUNCT_MAP.get(ch, ch)

            if mapped == '+':
                self.advance()
                if self.peek() == '+':
                    self.advance()
                    tokens.append(Token(TOKEN_PLUS_PLUS, '++', line_number, col))
                elif self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TOKEN_PLUS_EQ, '+=', line_number, col))
                else:
                    tokens.append(Token(TOKEN_PLUS, '+', line_number, col))
                continue

            if mapped == '-':
                self.advance()
                if self.peek() == '-':
                    self.advance()
                    if self.peek() == '/':
                        self.advance()
                        tokens.append(Token(TOKEN_MINUS_SLASH, '--/', line_number, col))
                    else:
                        tokens.append(Token(TOKEN_MINUS_MINUS, '--', line_number, col))
                elif self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TOKEN_MINUS_EQ, '-=', line_number, col))
                else:
                    tokens.append(Token(TOKEN_MINUS, '-', line_number, col))
                continue

            if mapped == '*':
                self.advance()
                if self.peek() == '*':
                    self.advance()
                    tokens.append(Token(TOKEN_DOUBLE_STAR, '**', line_number, col))
                elif self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TOKEN_STAR_EQ, '*=', line_number, col))
                else:
                    tokens.append(Token(TOKEN_STAR, '*', line_number, col))
                continue

            if mapped == '/':
                self.advance()
                if self.peek() == '/':
                    self.advance()
                    if self.peek() == '=':
                        self.advance()
                        tokens.append(Token(TOKEN_SLASH_EQ, '/=', line_number, col))
                    else:
                        tokens.append(Token(TOKEN_DOUBLE_SLASH, '//', line_number, col))
                elif self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TOKEN_SLASH_EQ, '/=', line_number, col))
                else:
                    tokens.append(Token(TOKEN_SLASH, '/', line_number, col))
                continue

            if mapped == '%':
                self.advance()
                tokens.append(Token(TOKEN_PERCENT, '%', line_number, col))
                continue

            if mapped == '=':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TOKEN_EQEQ, '==', line_number, col))
                else:
                    tokens.append(Token(TOKEN_EQ, '=', line_number, col))
                continue

            if mapped == '!':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TOKEN_BANGEQ, '!=', line_number, col))
                else:
                    tokens.append(Token(TOKEN_BANG, '!', line_number, col))
                continue

            if mapped == '<':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TOKEN_LTE, '<=', line_number, col))
                else:
                    tokens.append(Token(TOKEN_LT, '<', line_number, col))
                continue

            if mapped == '>':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TOKEN_GTE, '>=', line_number, col))
                else:
                    tokens.append(Token(TOKEN_GT, '>', line_number, col))
                continue

            if mapped == '&':
                self.advance()
                if self.peek() == '&':
                    self.advance()
                    tokens.append(Token(TOKEN_AND_AND, '&&', line_number, col))
                else:
                    self.error(f"不支持的字符: {ch}")
                continue

            if mapped == ':':
                self.advance()
                tokens.append(Token(TOKEN_COLON, ':', line_number, col))
                continue

            if mapped == ',':
                self.advance()
                tokens.append(Token(TOKEN_COMMA, ',', line_number, col))
                continue

            if mapped == '.':
                self.advance()
                tokens.append(Token(TOKEN_DOT, '.', line_number, col))
                continue

            if mapped == '(':
                self.advance()
                tokens.append(Token(TOKEN_LPAREN, '(', line_number, col))
                continue

            if mapped == ')':
                self.advance()
                tokens.append(Token(TOKEN_RPAREN, ')', line_number, col))
                continue

            if mapped == '[':
                self.advance()
                tokens.append(Token(TOKEN_LBRACKET, '[', line_number, col))
                continue

            if mapped == ']':
                self.advance()
                tokens.append(Token(TOKEN_RBRACKET, ']', line_number, col))
                continue

            if mapped == '{':
                self.advance()
                tokens.append(Token(TOKEN_LBRACE, '{', line_number, col))
                continue

            if mapped == '}':
                self.advance()
                tokens.append(Token(TOKEN_RBRACE, '}', line_number, col))
                continue

            if mapped == '@':
                self.advance()
                tokens.append(Token(TOKEN_AT, '@', line_number, col))
                continue

            if mapped == '|':
                self.advance()
                tokens.append(Token(TOKEN_PIPE, '|', line_number, col))
                continue

            if mapped == '-':
                self.advance()
                if self.peek() == '>':
                    self.advance()
                    tokens.append(Token(TOKEN_ARROW, '->', line_number, col))
                else:
                    tokens.append(Token(TOKEN_MINUS, '-', line_number, col))
                continue

            self.error(f"不支持的字符: {ch}")

        while len(indent_stack) > 1:
            indent_stack.pop()
            tokens.append(Token(TOKEN_DEDENT, None, self.line, self.column))

        tokens.append(Token(TOKEN_EOF, None, self.line, self.column))
        return tokens
