from .utils import MeowError
from .lexer import (
    TOKEN_KEYWORD, TOKEN_IDENTIFIER, TOKEN_NUMBER, TOKEN_STRING, TOKEN_STRING_INTERP,
    TOKEN_INDENT, TOKEN_DEDENT, TOKEN_NEWLINE, TOKEN_EOF,
    TOKEN_PLUS, TOKEN_MINUS, TOKEN_STAR, TOKEN_SLASH,
    TOKEN_DOUBLE_SLASH, TOKEN_PERCENT, TOKEN_DOUBLE_STAR,
    TOKEN_EQ, TOKEN_EQEQ, TOKEN_BANG, TOKEN_BANGEQ,
    TOKEN_LT, TOKEN_GT, TOKEN_LTE, TOKEN_GTE,
    TOKEN_AND_AND, TOKEN_PLUS_PLUS, TOKEN_MINUS_MINUS, TOKEN_MINUS_SLASH,
    TOKEN_PLUS_EQ, TOKEN_MINUS_EQ, TOKEN_STAR_EQ, TOKEN_SLASH_EQ,
    TOKEN_COLON, TOKEN_COMMA, TOKEN_DOT,
    TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_LBRACKET, TOKEN_RBRACKET,
    TOKEN_LBRACE, TOKEN_RBRACE,
    TOKEN_AT, TOKEN_PIPE, TOKEN_ARROW,
)
from .ast_nodes import (
    Program, Block, Number, String, StringInterp, Identifier, Boolean, Null,
    BinaryOp, UnaryOp, Assignment, AugmentedAssign,
    FunctionCall, FunctionDef, Return, Lambda,
    If, ElifClause, For, While, Break, Continue,
    ListLiteral, DictLiteral, DictEntry, Index, ListComp,
    Property, ClassDef, Try, Raise, ErrorDef, Import, CrossLangBlock,
)

_METHOD_NAME_KEYWORDS = {'init'}
_PARAM_NAME_KEYWORDS = {'self', 'init'}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self._call_depth = 0

    def error(self, message):
        t = self.peek()
        raise MeowError(message, t.line, t.column)

    def peek(self, offset=0):
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def advance(self):
        t = self.peek()
        self.pos += 1
        return t

    def expect(self, type_):
        t = self.peek()
        if t.type != type_:
            self.error(f"期望 {type_}，实际得到 {t.type}（{t.value!r}）")
        return self.advance()

    def skip_newlines(self):
        while self.peek().type == TOKEN_NEWLINE:
            self.advance()

    def parse(self):
        statements = self.parse_program()
        return statements

    def parse_program(self):
        statements = []
        self.skip_newlines()
        while self.peek().type != TOKEN_EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self.skip_newlines()
        return Program(statements)

    def parse_statement(self):
        t = self.peek()

        if t.type == TOKEN_KEYWORD:
            kw = t.value
            if kw == 'if':
                return self.parse_if_statement()
            elif kw == 'for':
                return self.parse_for_statement()
            elif kw == 'while':
                return self.parse_while_statement()
            elif kw == 'break':
                self.advance()
                return Break(line=t.line)
            elif kw == 'continue':
                self.advance()
                return Continue(line=t.line)
            elif kw == 'def':
                return self.parse_function_def()
            elif kw == 'return':
                return self.parse_return()
            elif kw == 'class':
                return self.parse_class_def()
            elif kw == 'try':
                return self.parse_try()
            elif kw == 'raise':
                return self.parse_raise()
            elif kw == 'error':
                return self.parse_error_def()
            elif kw == 'import':
                return self.parse_import()
            elif kw == 'true':
                self.advance()
                return Boolean(True, line=t.line)
            elif kw == 'false':
                self.advance()
                return Boolean(False, line=t.line)
            elif kw == 'null':
                self.advance()
                return Null(line=t.line)
            elif kw == 'init':
                return self.parse_function_def()
            else:
                return self.parse_identifier_statement()

        if t.type == TOKEN_IDENTIFIER:
            return self.parse_identifier_statement()

        expr = self.parse_expression()
        return expr

    def parse_identifier_statement(self):
        expr = self.parse_expression()

        if self.peek().type == TOKEN_EQ:
            if not isinstance(expr, (Identifier, Property, Index)):
                self.error("赋值目标必须是标识符、属性或索引")
            self.advance()
            value = self.parse_expression()
            targets = [expr]
            while self.peek().type == TOKEN_EQ:
                if not isinstance(value, Identifier):
                    self.error("链式赋值的中间目标必须是标识符")
                targets.append(value)
                self.advance()
                value = self.parse_expression()
            result = value
            for target in reversed(targets):
                result = Assignment(target, result, line=expr.line if hasattr(expr, 'line') else 0)
            return result

        if self.peek().type in (
            TOKEN_PLUS_EQ, TOKEN_MINUS_EQ, TOKEN_STAR_EQ, TOKEN_SLASH_EQ
        ):
            if not isinstance(expr, (Identifier, Property, Index)):
                self.error("复合赋值目标必须是标识符、属性或索引")
            op_token = self.advance()
            op_map = {
                TOKEN_PLUS_EQ: '+=',
                TOKEN_MINUS_EQ: '-=',
                TOKEN_STAR_EQ: '*=',
                TOKEN_SLASH_EQ: '/=',
            }
            value = self.parse_expression()
            return AugmentedAssign(
                expr,
                op_map[op_token.type],
                value,
                line=expr.line if hasattr(expr, 'line') else 0,
            )

        if isinstance(expr, (Property, Index)):
            if self._is_call_arg_start(self.peek()):
                args = self.parse_argument_list()
            else:
                args = []
            expr = FunctionCall(expr, args, line=expr.line if hasattr(expr, 'line') else 0)

        return expr

    def parse_argument_list(self):
        args = []
        if self.peek().type in (TOKEN_NEWLINE, TOKEN_DEDENT, TOKEN_EOF):
            return args
        self._call_depth += 1
        try:
            while True:
                self._call_depth -= 1
                try:
                    expr = self.parse_expression()
                finally:
                    self._call_depth += 1
                args.append(expr)
                if self._call_depth <= 1 and self._is_call_arg_start(self.peek()):
                    continue
                if self.peek().type == TOKEN_COMMA:
                    self.advance()
                    continue
                break
        finally:
            self._call_depth -= 1
        return args

    def parse_if_statement(self):
        line = self.advance().line
        condition = self.parse_expression()
        self.expect(TOKEN_NEWLINE)
        then_block = self.parse_block()
        elif_clauses = []
        else_block = None
        while self.peek().type == TOKEN_KEYWORD and self.peek().value == 'elif':
            self.advance()
            elif_cond = self.parse_expression()
            self.expect(TOKEN_NEWLINE)
            elif_block = self.parse_block()
            elif_clauses.append(ElifClause(elif_cond, elif_block, line=line))
        if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'else':
            self.advance()
            self.expect(TOKEN_NEWLINE)
            else_block = self.parse_block()
        return If(condition, then_block, elif_clauses, else_block, line=line)

    def parse_for_statement(self):
        line = self.advance().line
        var_tok = self.expect(TOKEN_IDENTIFIER)
        var = Identifier(var_tok.value, line=var_tok.line)
        kw = self.peek()
        if kw.type == TOKEN_KEYWORD and kw.value == 'in':
            self.advance()
        iterable = self.parse_expression()
        self.expect(TOKEN_NEWLINE)
        body = self.parse_block()
        return For(var, iterable, body, line=line)

    def parse_while_statement(self):
        line = self.advance().line
        condition = self.parse_expression()
        self.expect(TOKEN_NEWLINE)
        body = self.parse_block()
        return While(condition, body, line=line)

    def parse_function_def(self):
        line = self.peek().line
        if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'def':
            self.advance()
        name_tok = self.peek()
        if name_tok.type == TOKEN_IDENTIFIER:
            name = self.advance().value
        elif name_tok.type == TOKEN_KEYWORD and name_tok.value in _METHOD_NAME_KEYWORDS:
            self.advance()
            name = name_tok.value
        else:
            self.error(f"期望函数名，实际得到 {name_tok.type}（{name_tok.value!r}）")
        params = []
        while self.peek().type == TOKEN_IDENTIFIER or (
            self.peek().type == TOKEN_KEYWORD and self.peek().value in _PARAM_NAME_KEYWORDS
        ):
            param_tok = self.advance()
            params.append(Identifier(param_tok.value, line=param_tok.line))
            if self.peek().type == TOKEN_COMMA:
                self.advance()
        self.expect(TOKEN_NEWLINE)
        body = self.parse_block()
        return FunctionDef(name, params, body, line=line)

    def parse_return(self):
        line = self.advance().line
        if self.peek().type in (TOKEN_NEWLINE, TOKEN_DEDENT, TOKEN_EOF):
            return Return(None, line=line)
        expr = self.parse_expression()
        return Return(expr, line=line)

    def parse_class_def(self):
        line = self.advance().line
        name_tok = self.expect(TOKEN_IDENTIFIER)
        name = name_tok.value
        base_class = None
        if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'extends':
            self.advance()
            base_tok = self.expect(TOKEN_IDENTIFIER)
            base_class = Identifier(base_tok.value, line=base_tok.line)
        elif self.peek().type == TOKEN_KEYWORD and self.peek().value == 'implements':
            self.advance()
            iface_tok = self.expect(TOKEN_IDENTIFIER)
            base_class = Identifier(iface_tok.value, line=iface_tok.line)
        self.expect(TOKEN_NEWLINE)
        body = self.parse_block()
        methods = []
        for stmt in body.statements:
            if isinstance(stmt, FunctionDef):
                methods.append(stmt)
        return ClassDef(name, base_class, methods, line=line)

    def parse_try(self):
        line = self.advance().line
        self.expect(TOKEN_NEWLINE)
        try_block = self.parse_block()
        except_var = None
        except_block = None
        if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'except':
            self.advance()
            if self.peek().type == TOKEN_IDENTIFIER:
                var_tok = self.expect(TOKEN_IDENTIFIER)
                except_var = Identifier(var_tok.value, line=var_tok.line)
            self.expect(TOKEN_NEWLINE)
            except_block = self.parse_block()
        finally_block = None
        if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'finally':
            self.advance()
            self.expect(TOKEN_NEWLINE)
            finally_block = self.parse_block()
        return Try(try_block, except_var, except_block, finally_block, line=line)

    def parse_raise(self):
        line = self.advance().line
        name_tok = self.expect(TOKEN_IDENTIFIER)
        message = None
        if self.peek().type != TOKEN_NEWLINE and self.peek().type != TOKEN_DEDENT:
            message = self.parse_expression()
        return Raise(name_tok.value, message, line=line)

    def parse_error_def(self):
        line = self.advance().line
        name_tok = self.expect(TOKEN_IDENTIFIER)
        message = None
        if self.peek().type != TOKEN_NEWLINE and self.peek().type != TOKEN_DEDENT:
            message = self.parse_expression()
        return ErrorDef(name_tok.value, message, line=line)

    def parse_import(self):
        line = self.advance().line
        lang_tok = self.expect(TOKEN_IDENTIFIER)
        lang = lang_tok.value
        self.expect(TOKEN_LBRACE)
        self.skip_newlines()
        body_parts = []
        depth = 1
        while self.peek().type != TOKEN_EOF and depth > 0:
            if self.peek().type == TOKEN_LBRACE:
                depth += 1
            elif self.peek().type == TOKEN_RBRACE:
                depth -= 1
                if depth == 0:
                    break
            tok = self.advance()
            if tok.type == TOKEN_NEWLINE:
                body_parts.append('\n')
            elif tok.type == TOKEN_INDENT:
                pass
            elif tok.type == TOKEN_DEDENT:
                pass
            else:
                body_parts.append(str(tok.value) if tok.value is not None else '')
                body_parts.append(' ')
        self.expect(TOKEN_RBRACE)
        if self.peek().type == TOKEN_DOT:
            self.advance()
            if self.peek().type == TOKEN_IDENTIFIER:
                self.advance()
        return CrossLangBlock(lang, ''.join(body_parts).strip(), line=line)

    def parse_block(self):
        statements = []
        self.skip_newlines()
        indent_tok = self.peek()
        if indent_tok.type != TOKEN_INDENT:
            self.error("期望缩进块")
        self.advance()
        while self.peek().type not in (TOKEN_DEDENT, TOKEN_EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self.skip_newlines()
        if self.peek().type == TOKEN_DEDENT:
            self.advance()
        return Block(statements)

    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.peek().type == TOKEN_KEYWORD and self.peek().value == 'or':
            self.advance()
            right = self.parse_and()
            left = BinaryOp(left, 'or', right, line=left.line if hasattr(left, 'line') else 0)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.peek().type == TOKEN_KEYWORD and self.peek().value == 'and':
            self.advance()
            right = self.parse_not()
            left = BinaryOp(left, 'and', right, line=left.line if hasattr(left, 'line') else 0)
        return left

    def parse_not(self):
        if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'not':
            self.advance()
            operand = self.parse_not()
            return UnaryOp('not', operand, line=operand.line if hasattr(operand, 'line') else 0)
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_set_op()
        while self.peek().type in (
            TOKEN_EQEQ, TOKEN_BANGEQ, TOKEN_LT, TOKEN_GT, TOKEN_LTE, TOKEN_GTE,
        ):
            op = self.advance()
            op_map = {
                TOKEN_EQEQ: '==',
                TOKEN_BANGEQ: '!=',
                TOKEN_LT: '<',
                TOKEN_GT: '>',
                TOKEN_LTE: '<=',
                TOKEN_GTE: '>=',
            }
            right = self.parse_set_op()
            left = BinaryOp(left, op_map[op.type], right, line=left.line if hasattr(left, 'line') else 0)
        if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'in':
            self.advance()
            right = self.parse_set_op()
            left = BinaryOp(left, 'in', right, line=left.line if hasattr(left, 'line') else 0)
        if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'not':
            if self.peek(1).type == TOKEN_KEYWORD and self.peek(1).value == 'in':
                self.advance()
                self.advance()
                right = self.parse_set_op()
                left = BinaryOp(left, 'not in', right, line=left.line if hasattr(left, 'line') else 0)
        return left

    def parse_set_op(self):
        left = self.parse_term()
        while self.peek().type in (
            TOKEN_PLUS_PLUS, TOKEN_MINUS_MINUS, TOKEN_MINUS_SLASH, TOKEN_AND_AND,
        ):
            op = self.advance()
            op_map = {
                TOKEN_PLUS_PLUS: '++',
                TOKEN_MINUS_MINUS: '--',
                TOKEN_MINUS_SLASH: '--/',
                TOKEN_AND_AND: '&&',
            }
            right = self.parse_term()
            left = BinaryOp(left, op_map[op.type], right, line=left.line if hasattr(left, 'line') else 0)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.peek().type in (TOKEN_PLUS, TOKEN_MINUS):
            op = self.advance()
            op_map = {TOKEN_PLUS: '+', TOKEN_MINUS: '-'}
            right = self.parse_factor()
            left = BinaryOp(left, op_map[op.type], right, line=left.line if hasattr(left, 'line') else 0)
        return left

    def parse_factor(self):
        left = self.parse_unary()
        while self.peek().type in (TOKEN_STAR, TOKEN_SLASH, TOKEN_DOUBLE_SLASH, TOKEN_PERCENT):
            op = self.advance()
            op_map = {
                TOKEN_STAR: '*',
                TOKEN_SLASH: '/',
                TOKEN_DOUBLE_SLASH: '//',
                TOKEN_PERCENT: '%',
            }
            right = self.parse_unary()
            left = BinaryOp(left, op_map[op.type], right, line=left.line if hasattr(left, 'line') else 0)
        return left

    def parse_unary(self):
        if self.peek().type == TOKEN_MINUS:
            op = self.advance()
            operand = self.parse_unary()
            return UnaryOp('-', operand, line=op.line)
        return self.parse_power()

    def parse_power(self):
        left = self.parse_call()
        if self.peek().type == TOKEN_DOUBLE_STAR:
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, '**', right, line=left.line if hasattr(left, 'line') else 0)
        return left

    def _is_call_arg_start(self, tok):
        if tok.type in (TOKEN_NUMBER, TOKEN_STRING, TOKEN_IDENTIFIER, TOKEN_LPAREN, TOKEN_LBRACKET):
            return True
        if tok.type == TOKEN_KEYWORD and tok.value in ('true', 'false', 'null', 'fn', 'not', 'self'):
            return True
        return False

    def parse_call(self):
        left = self.parse_primary()

        while True:
            t = self.peek()

            if t.type == TOKEN_LPAREN:
                self.advance()
                args = []
                if self.peek().type != TOKEN_RPAREN:
                    while True:
                        self._call_depth += 1
                        try:
                            args.append(self.parse_expression())
                        finally:
                            self._call_depth -= 1
                        if self.peek().type == TOKEN_COMMA:
                            self.advance()
                        else:
                            break
                self.expect(TOKEN_RPAREN)
                line = left.line if hasattr(left, 'line') else 0
                left = FunctionCall(left, args, line=line)
                continue

            if t.type == TOKEN_LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TOKEN_RBRACKET)
                left = Index(left, index, line=left.line if hasattr(left, 'line') else 0)
                continue

            if t.type == TOKEN_DOT:
                self.advance()
                prop_tok = self.peek()
                if prop_tok.type == TOKEN_IDENTIFIER:
                    prop = self.advance()
                elif prop_tok.type == TOKEN_KEYWORD and prop_tok.value in _METHOD_NAME_KEYWORDS:
                    prop = self.advance()
                elif prop_tok.type == TOKEN_NUMBER:
                    prop = self.advance()
                elif prop_tok.type == TOKEN_STRING:
                    prop = self.advance()
                else:
                    self.error(f"期望属性名，实际得到 {prop_tok.type}（{prop_tok.value!r}）")
                left = Property(left, str(prop.value), line=left.line if hasattr(left, 'line') else 0)
                continue

            if self._call_depth == 0 and isinstance(left, (Identifier, FunctionCall, Property, Index)) and self._is_call_arg_start(t):
                args = self.parse_argument_list()
                line = left.line if hasattr(left, 'line') else 0
                left = FunctionCall(left, args, line=line)
                continue

            break

        return left

    def parse_primary(self):
        t = self.advance()
        line = t.line

        if t.type == TOKEN_NUMBER:
            return Number(t.value, line=line)

        if t.type == TOKEN_STRING:
            return self._parse_string_with_interp(t.value, line)

        if t.type == TOKEN_STRING_INTERP:
            return StringInterp(t.value, line=line)

        if t.type == TOKEN_IDENTIFIER:
            return Identifier(t.value, line=line)

        if t.type == TOKEN_KEYWORD:
            if t.value == 'true':
                return Boolean(True, line=line)
            if t.value == 'false':
                return Boolean(False, line=line)
            if t.value == 'null':
                return Null(line=line)
            if t.value == 'fn':
                return self.parse_lambda(line)
            if t.value in _PARAM_NAME_KEYWORDS:
                return Identifier(t.value, line=line)

        if t.type == TOKEN_LBRACKET:
            return self.parse_list_literal(line)

        if t.type == TOKEN_LPAREN:
            expr = self.parse_expression()
            self.expect(TOKEN_RPAREN)
            return expr

        if t.type == TOKEN_MINUS:
            operand = self.parse_primary()
            return UnaryOp('-', operand, line=line)

        self.error(f"意外的 token: {t.type} ({t.value!r})")

    def _parse_string_with_interp(self, value, line):
        parts = []
        i = 0
        buf = []
        while i < len(value):
            ch = value[i]
            if ch == '/' and i + 1 < len(value):
                next_ch = value[i + 1]
                if next_ch == '/':
                    buf.append('/')
                    i += 2
                    continue
                elif next_ch == '(':
                    if buf:
                        parts.append(('str', ''.join(buf)))
                        buf = []
                    i += 2
                    depth = 1
                    expr_chars = []
                    while i < len(value) and depth > 0:
                        if value[i] == '(':
                            depth += 1
                        elif value[i] == ')':
                            depth -= 1
                            if depth == 0:
                                break
                        expr_chars.append(value[i])
                        i += 1
                    i += 1
                    expr_str = ''.join(expr_chars)
                    parts.append(('interp_expr', expr_str))
                    continue
                elif next_ch.isalpha() or next_ch == '_':
                    if buf:
                        parts.append(('str', ''.join(buf)))
                        buf = []
                    i += 1
                    var_chars = []
                    while i < len(value):
                        ch2 = value[i]
                        if ch2.isalnum() or ch2 == '_':
                            var_chars.append(ch2)
                            i += 1
                        else:
                            break
                    # 支持属性访问和索引访问: /self.name /self.name[1]
                    expr_chars = list(var_chars)
                    while i < len(value):
                        if value[i] == '.':
                            expr_chars.append(value[i])
                            i += 1
                            while i < len(value) and (value[i].isalnum() or value[i] == '_'):
                                expr_chars.append(value[i])
                                i += 1
                        elif value[i] == '[':
                            expr_chars.append(value[i])
                            i += 1
                            bracket_depth = 1
                            while i < len(value) and bracket_depth > 0:
                                if value[i] == '[':
                                    bracket_depth += 1
                                elif value[i] == ']':
                                    bracket_depth -= 1
                                expr_chars.append(value[i])
                                i += 1
                        else:
                            break
                    if len(expr_chars) > len(var_chars):
                        parts.append(('interp_expr', ''.join(expr_chars)))
                    else:
                        parts.append(('interp_var', ''.join(var_chars)))
                    continue
            buf.append(ch)
            i += 1

        if buf:
            parts.append(('str', ''.join(buf)))

        if len(parts) == 1 and parts[0][0] == 'str':
            return String(parts[0][1], line=line)

        return StringInterp(parts, line=line)

    def parse_lambda(self, line):
        params = []
        while self.peek().type == TOKEN_IDENTIFIER or (
            self.peek().type == TOKEN_KEYWORD and self.peek().value in _PARAM_NAME_KEYWORDS
        ):
            param_tok = self.advance()
            params.append(Identifier(param_tok.value, line=param_tok.line))
        if self.peek().type == TOKEN_MINUS_MINUS:
            self.advance()
        body = self.parse_expression()
        return Lambda(params, body, line=line)

    def parse_list_literal(self, line):
        elements = []
        entries = []
        is_dict = False

        self.skip_newlines()

        if self.peek().type == TOKEN_RBRACKET:
            self.advance()
            return ListLiteral([], line=line)

        while True:
            self.skip_newlines()
            if self.peek().type == TOKEN_RBRACKET:
                break

            key = self.parse_expression()

            self.skip_newlines()

            if self.peek().type == TOKEN_COLON:
                is_dict = True
                self.advance()
                self.skip_newlines()
                value = self.parse_expression()
                entries.append(DictEntry(key, value, line=key.line if hasattr(key, 'line') else line))
            else:
                elements.append(key)

            self.skip_newlines()

            if self.peek().type == TOKEN_COMMA:
                self.advance()
            elif self.peek().type == TOKEN_RBRACKET:
                break
            else:
                break

        if not is_dict and len(elements) == 1:
            if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'for':
                self.advance()
                var_tok = self.expect(TOKEN_IDENTIFIER)
                var = Identifier(var_tok.value, line=var_tok.line)
                kw = self.peek()
                if kw.type == TOKEN_KEYWORD and kw.value == 'in':
                    self.advance()
                iterable = self.parse_expression()
                self.expect(TOKEN_RBRACKET)
                return ListComp(elements[0], var, iterable, line=line)

        self.expect(TOKEN_RBRACKET)

        if is_dict:
            return DictLiteral(entries, line=line)

        return ListLiteral(elements, line=line)
