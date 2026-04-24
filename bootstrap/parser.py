from .utils import MeowError
from .lexer import (
    TOKEN_KEYWORD, TOKEN_IDENTIFIER, TOKEN_NUMBER, TOKEN_STRING,
    TOKEN_INDENT, TOKEN_DEDENT, TOKEN_NEWLINE, TOKEN_EOF,
    TOKEN_PLUS, TOKEN_MINUS, TOKEN_STAR, TOKEN_SLASH,
    TOKEN_DOUBLE_SLASH, TOKEN_PERCENT, TOKEN_DOUBLE_STAR,
    TOKEN_EQ, TOKEN_EQEQ, TOKEN_BANG, TOKEN_BANGEQ,
    TOKEN_LT, TOKEN_GT, TOKEN_LTE, TOKEN_GTE,
    TOKEN_AND_AND, TOKEN_PLUS_PLUS, TOKEN_MINUS_MINUS, TOKEN_MINUS_SLASH,
    TOKEN_PLUS_EQ, TOKEN_MINUS_EQ, TOKEN_STAR_EQ, TOKEN_SLASH_EQ,
    TOKEN_COLON, TOKEN_COMMA, TOKEN_DOT,
    TOKEN_LPAREN, TOKEN_RPAREN, TOKEN_LBRACKET, TOKEN_RBRACKET,
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


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

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
                name = self.advance()
                return Identifier(name.value, line=name.line)
            # 'and'/'or'/'not' are handled in expression parsing
            # 'fn' for lambda is handled in expression parsing

        if t.type == TOKEN_IDENTIFIER:
            return self.parse_identifier_statement()

        expr = self.parse_expression()
        return expr

    def parse_identifier_statement(self):
        t = self.advance()
        name = t.value

        if self.peek().type == TOKEN_EQ:
            self.advance()
            value = self.parse_expression()
            # 链式赋值: a = b = 5 → a = (b = 5)
            # a = b = c = 5 → a = (b = (c = 5))
            targets = [Identifier(name, line=t.line)]
            while self.peek().type == TOKEN_EQ:
                if not isinstance(value, Identifier):
                    self.error("链式赋值的中间目标必须是标识符")
                targets.append(value)
                self.advance()
                value = self.parse_expression()
            result = value
            for target in reversed(targets):
                result = Assignment(target, result, line=t.line)
            return result

        if self.peek().type in (
            TOKEN_PLUS_EQ, TOKEN_MINUS_EQ, TOKEN_STAR_EQ, TOKEN_SLASH_EQ
        ):
            op_token = self.advance()
            op_map = {
                TOKEN_PLUS_EQ: '+=',
                TOKEN_MINUS_EQ: '-=',
                TOKEN_STAR_EQ: '*=',
                TOKEN_SLASH_EQ: '/=',
            }
            value = self.parse_expression()
            return AugmentedAssign(
                Identifier(name, line=t.line),
                op_map[op_token.type],
                value,
                line=t.line,
            )

        args = self.parse_argument_list()
        return FunctionCall(Identifier(name, line=t.line), args, line=t.line)

    def parse_argument_list(self):
        args = []
        if self.peek().type in (TOKEN_NEWLINE, TOKEN_DEDENT, TOKEN_EOF):
            return args
        while True:
            expr = self.parse_expression()
            args.append(expr)
            if self._is_call_arg_start(self.peek()):
                continue
            if self.peek().type == TOKEN_COMMA:
                self.advance()
                continue
            break
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
        line = self.advance().line
        name_tok = self.expect(TOKEN_IDENTIFIER)
        name = name_tok.value
        params = []
        while self.peek().type == TOKEN_IDENTIFIER:
            param_tok = self.advance()
            params.append(Identifier(param_tok.value, line=param_tok.line))
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
        self.expect(TOKEN_LBRACKET)
        self.skip_newlines()
        body_lines = []
        depth = 1
        while self.peek().type != TOKEN_EOF and depth > 0:
            if self.peek().type == TOKEN_LBRACKET:
                depth += 1
            elif self.peek().type == TOKEN_RBRACKET:
                depth -= 1
                if depth == 0:
                    break
            body_lines.append(self.advance().value if self.peek().value is not None else '')
        self.expect(TOKEN_RBRACKET)
        self.expect(TOKEN_DOT)
        after_call = self.expect(TOKEN_IDENTIFIER)
        # Cross-language block, parse as expression that returns the result
        return CrossLangBlock(lang, '\n'.join(body_lines), line=line)

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
        # Handle 'in'
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
        if tok.type == TOKEN_KEYWORD and tok.value in ('true', 'false', 'null', 'fn'):
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
                        args.append(self.parse_expression())
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
                prop = self.expect(TOKEN_IDENTIFIER)
                left = Property(left, prop.value, line=left.line if hasattr(left, 'line') else 0)
                continue

            if isinstance(left, (Identifier, FunctionCall, Property, Index)) and self._is_call_arg_start(t):
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
        while self.peek().type == TOKEN_IDENTIFIER:
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

        self.expect(TOKEN_RBRACKET)

        if is_dict:
            return DictLiteral(entries, line=line)

        if self.peek().type == TOKEN_KEYWORD and self.peek().value == 'for':
            self.advance()
            var_tok = self.expect(TOKEN_IDENTIFIER)
            var = Identifier(var_tok.value, line=var_tok.line)
            kw = self.peek()
            if kw.type == TOKEN_KEYWORD and kw.value == 'in':
                self.advance()
            iterable = self.parse_expression()
            return ListComp(elements[0] if elements else Null(), var, iterable, line=line)

        return ListLiteral(elements, line=line)
