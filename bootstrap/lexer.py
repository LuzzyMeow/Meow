from .utils import MeowError

# Token types
TOKEN_KEYWORD = 'KEYWORD'
TOKEN_IDENTIFIER = 'IDENTIFIER'
TOKEN_NUMBER = 'NUMBER'
TOKEN_STRING = 'STRING'
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
TOKEN_AT = 'AT'
TOKEN_PIPE = 'PIPE'
TOKEN_ARROW = 'ARROW'

KEYWORDS = {
    'if', 'elif', 'else', 'for', 'while',
    'break', 'continue', 'def', 'return',
    'class', 'init', 'self', 'super', 'interface', 'implements',
    'import', 'from', 'as',
    'try', 'except', 'finally', 'raise', 'error',
    'async', 'await', 'match', 'case',
    'and', 'or', 'not', 'true', 'false',
    'null', 'const', 'enum', 'extends', 'fn', 'in', 'all',
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
        self.tokens = []

    def error(self, message):
        raise MeowError(message, self.line, self.column)

    def peek(self, offset=0):
        idx = self.pos + offset
        if idx >= len(self.source):
            return '\0'
        return self.source[idx]

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.source) and self.peek() in (' ', '\t'):
            self.advance()

    def read_string(self, quote):
        result = []
        while self.pos < len(self.source):
            ch = self.advance()
            if ch == '\\':
                esc = self.advance()
                if esc == 'n':
                    result.append('\n')
                elif esc == 't':
                    result.append('\t')
                elif esc == '\\':
                    result.append('\\')
                elif esc == '"':
                    result.append('"')
                elif esc == "'":
                    result.append("'")
                else:
                    result.append('\\' + esc)
            elif ch == quote:
                break
            else:
                result.append(ch)
        else:
            self.error(f"未闭合的字符串，缺少 {quote}")
        return ''.join(result)

    def read_number(self):
        start = self.pos
        is_float = False
        while self.pos < len(self.source):
            ch = self.peek()
            if ch.isdigit():
                self.advance()
            elif ch == '.' and not is_float:
                next_ch = self.peek(1)
                if next_ch.isdigit():
                    is_float = True
                    self.advance()
                else:
                    break
            elif ch in ('e', 'E'):
                is_float = True
                self.advance()
                if self.peek() in ('+', '-'):
                    self.advance()
            else:
                break
        text = self.source[start:self.pos]
        if text.startswith('0x') or text.startswith('0X'):
            return int(text, 16)
        if text.startswith('0b') or text.startswith('0B'):
            return int(text, 2)
        if is_float:
            return float(text)
        return int(text)

    def read_identifier(self):
        start = self.pos
        while self.pos < len(self.source):
            ch = self.peek()
            if ch.isalnum() or ch == '_':
                self.advance()
            else:
                break
        word = self.source[start:self.pos]
        return word

    def map_chinese_punct(self, ch):
        if ch in _CHINESE_PUNCT_MAP:
            return _CHINESE_PUNCT_MAP[ch]
        return ch

    def tokenize_line(self, line_text, line_number):
        tokens = []
        self.pos = 0
        self.column = 1

        while self.pos < len(line_text):
            ch = self.peek()

            if ch in (' ', '\t'):
                self.skip_whitespace()
                continue

            if ch == '#':
                break

            mapped = self.map_chinese_punct(ch)

            col = self.column

            if ch in _CHINESE_OPEN_PUNCT:
                mapped = '(' if ch in ('\uff08',) else '['
            elif ch in _CHINESE_CLOSE_PUNCT:
                mapped = ')' if ch in ('\uff09',) else ']'

            if mapped in ('"', "'"):
                self.advance()
                value = self.read_string(ch if ch in ('"', "'") else mapped)
                tokens.append(Token(TOKEN_STRING, value, line_number, col))
                continue

            if mapped.isdigit() or (mapped == '.' and self.peek(1) and self.peek(1).isdigit()):
                start = self.pos
                self.advance()
                num_text = mapped
                while self.pos < len(line_text):
                    nc = self.peek()
                    nm = self.map_chinese_punct(nc)
                    if nm.isdigit():
                        num_text += nc
                        self.advance()
                    elif nm == '.' and not ('e' in num_text or 'E' in num_text):
                        nn = self.peek(1)
                        if nn and self.map_chinese_punct(nn).isdigit():
                            num_text += nc
                            self.advance()
                        else:
                            break
                    elif nm in ('e', 'E') and not ('e' in num_text or 'E' in num_text):
                        num_text += nc
                        self.advance()
                        nn = self.peek()
                        if nn and self.map_chinese_punct(nn) in ('+', '-'):
                            num_text += nn
                            self.advance()
                    else:
                        break
                if num_text.startswith('0x') or num_text.startswith('0X'):
                    tokens.append(Token(TOKEN_NUMBER, int(num_text, 16), line_number, col))
                elif num_text.startswith('0b') or num_text.startswith('0B'):
                    tokens.append(Token(TOKEN_NUMBER, int(num_text, 2), line_number, col))
                elif '.' in num_text or 'e' in num_text or 'E' in num_text:
                    tokens.append(Token(TOKEN_NUMBER, float(num_text), line_number, col))
                else:
                    tokens.append(Token(TOKEN_NUMBER, int(num_text), line_number, col))
                continue

            if mapped.isalpha() or mapped == '_':
                word = mapped
                self.advance()
                while self.pos < len(line_text):
                    nc = self.peek()
                    nm = self.map_chinese_punct(nc)
                    if nm.isalnum() or nm == '_':
                        word += nc
                        self.advance()
                    else:
                        break
                if word in KEYWORDS:
                    if word in ('true', 'false'):
                        tokens.append(Token(TOKEN_KEYWORD, word, line_number, col))
                    else:
                        tokens.append(Token(TOKEN_KEYWORD, word, line_number, col))
                else:
                    tokens.append(Token(TOKEN_IDENTIFIER, word, line_number, col))
                continue

            if mapped == '=':
                if self.peek(1) and self.map_chinese_punct(self.peek(1)) == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_EQEQ, '==', line_number, col))
                else:
                    self.advance()
                    tokens.append(Token(TOKEN_EQ, '=', line_number, col))
                continue

            if mapped == '!':
                if self.peek(1) and self.map_chinese_punct(self.peek(1)) == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_BANGEQ, '!=', line_number, col))
                else:
                    self.advance()
                    tokens.append(Token(TOKEN_BANG, '!', line_number, col))
                continue

            if mapped == '>':
                if self.peek(1) and self.map_chinese_punct(self.peek(1)) == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_GTE, '>=', line_number, col))
                else:
                    self.advance()
                    tokens.append(Token(TOKEN_GT, '>', line_number, col))
                continue

            if mapped == '<':
                if self.peek(1) and self.map_chinese_punct(self.peek(1)) == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_LTE, '<=', line_number, col))
                else:
                    self.advance()
                    tokens.append(Token(TOKEN_LT, '<', line_number, col))
                continue

            if mapped == '+':
                next_ch = self.peek(1)
                nm2 = self.map_chinese_punct(next_ch) if next_ch else '\0'
                if nm2 == '+':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_PLUS_PLUS, '++', line_number, col))
                elif nm2 == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_PLUS_EQ, '+=', line_number, col))
                else:
                    self.advance()
                    tokens.append(Token(TOKEN_PLUS, '+', line_number, col))
                continue

            if mapped == '-':
                next_ch = self.peek(1)
                nm2 = self.map_chinese_punct(next_ch) if next_ch else '\0'
                if nm2 == '-':
                    nnm = self.peek(2)
                    nm3 = self.map_chinese_punct(nnm) if nnm else '\0'
                    if nm3 == '/':
                        self.advance()
                        self.advance()
                        self.advance()
                        tokens.append(Token(TOKEN_MINUS_SLASH, '--/', line_number, col))
                    elif nm3 == '=':
                        self.advance()
                        self.advance()
                        self.advance()
                        tokens.append(Token(TOKEN_MINUS_EQ, '-=', line_number, col))
                    else:
                        self.advance()
                        self.advance()
                        tokens.append(Token(TOKEN_MINUS_MINUS, '--', line_number, col))
                elif nm2 == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_MINUS_EQ, '-=', line_number, col))
                else:
                    self.advance()
                    tokens.append(Token(TOKEN_MINUS, '-', line_number, col))
                continue

            if mapped == '*':
                next_ch = self.peek(1)
                nm2 = self.map_chinese_punct(next_ch) if next_ch else '\0'
                if nm2 == '*':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_DOUBLE_STAR, '**', line_number, col))
                elif nm2 == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_STAR_EQ, '*=', line_number, col))
                else:
                    self.advance()
                    tokens.append(Token(TOKEN_STAR, '*', line_number, col))
                continue

            if mapped == '/':
                next_ch = self.peek(1)
                nm2 = self.map_chinese_punct(next_ch) if next_ch else '\0'
                if nm2 == '/':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_DOUBLE_SLASH, '//', line_number, col))
                elif nm2 == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TOKEN_SLASH_EQ, '/=', line_number, col))
                else:
                    self.advance()
                    tokens.append(Token(TOKEN_SLASH, '/', line_number, col))
                continue

            if mapped == '%':
                self.advance()
                tokens.append(Token(TOKEN_PERCENT, '%', line_number, col))
                continue

            if mapped == ',':
                self.advance()
                tokens.append(Token(TOKEN_COMMA, ',', line_number, col))
                continue

            if mapped == ':':
                self.advance()
                tokens.append(Token(TOKEN_COLON, ':', line_number, col))
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

            if mapped == '@':
                self.advance()
                tokens.append(Token(TOKEN_AT, '@', line_number, col))
                continue

            if mapped == '|':
                self.advance()
                tokens.append(Token(TOKEN_PIPE, '|', line_number, col))
                continue

            self.advance()

        return tokens

    def tokenize(self):
        lines = self.source.split('\n')
        result = []
        indent_stack = [0]

        for i, line_text in enumerate(lines):
            line_number = i + 1
            stripped = line_text.lstrip()
            if stripped == '' or stripped.startswith('#'):
                continue
            indent = len(line_text) - len(stripped)
            if indent % 4 != 0:
                pass
            if indent > indent_stack[-1]:
                indent_stack.append(indent)
                result.append(Token(TOKEN_INDENT, None, line_number, 1))
            elif indent < indent_stack[-1]:
                while indent_stack and indent < indent_stack[-1]:
                    indent_stack.pop()
                    result.append(Token(TOKEN_DEDENT, None, line_number, 1))
                if indent_stack and indent != indent_stack[-1]:
                    raise MeowError(f"缩进层级不匹配，期望 {indent_stack[-1]} 空格，实际 {indent} 空格", line_number, 1)
            line_tokens = self.tokenize_line(line_text.strip(), line_number)
            result.extend(line_tokens)
            result.append(Token(TOKEN_NEWLINE, None, line_number, len(line_text) + 1))

        while len(indent_stack) > 1:
            indent_stack.pop()
            result.append(Token(TOKEN_DEDENT, None, line_number, 1))

        result.append(Token(TOKEN_EOF, None, line_number, 1))
        return result
