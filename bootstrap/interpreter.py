import sys

from .utils import MeowRuntimeError
from .ast_nodes import (
    Program, Block, Number, String, StringInterp, Identifier, Boolean, Null,
    BinaryOp, UnaryOp, Assignment, AugmentedAssign,
    FunctionCall, FunctionDef, Return, Lambda,
    If, ElifClause, For, While, Break, Continue,
    ListLiteral, DictLiteral, DictEntry, Index, ListComp,
    Property, ClassDef, Try, Raise, ErrorDef, Import, CrossLangBlock,
)
from .environment import (
    Environment, MeowReturn, MeowBreak, MeowContinue, MeowException,
    MeowFunction, MeowLambda, MeowClass, MeowInstance, MeowList, MeowDict,
    NULL_VALUE,
)
from .builtins import register_builtins
from .cross_lang import CrossLangBridge


class Interpreter:
    def __init__(self):
        self.env = Environment()
        register_builtins(self.env)
        self.error_classes = {}
        self.cross_lang = CrossLangBridge()

    def error(self, message, node=None):
        line = node.line if node is not None and hasattr(node, 'line') else None
        raise MeowRuntimeError(message, line=line)

    def interpret(self, program):
        try:
            return self.visit(program)
        except MeowException as e:
            print(e)
            return NULL_VALUE
        except MeowRuntimeError as e:
            print(e)
            sys.exit(1)

    def visit(self, node):
        if node is None:
            return NULL_VALUE
        method = f'visit_{type(node).__name__}'
        visitor = getattr(self, method, None)
        if visitor is None:
            self.error(f"不支持访问节点类型: {type(node).__name__}", node)
        return visitor(node)

    def visit_Program(self, node):
        result = NULL_VALUE
        for stmt in node.statements:
            result = self.visit(stmt)
            if isinstance(result, MeowReturn):
                raise result
        return result

    def visit_Block(self, node):
        env = Environment(self.env)
        old_env = self.env
        self.env = env
        try:
            for stmt in node.statements:
                result = self.visit(stmt)
                if isinstance(result, (MeowReturn, MeowBreak, MeowContinue)):
                    return result
            return NULL_VALUE
        finally:
            self.env = old_env

    def visit_Number(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_StringInterp(self, node):
        result = []
        for part_type, part_value in node.parts:
            if part_type == 'str':
                result.append(part_value)
            elif part_type == 'interp_var':
                val = self.env.get(part_value)
                result.append(str(val))
            elif part_type == 'interp_expr':
                from .lexer import Lexer
                from .parser import Parser
                lexer = Lexer(part_value)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse_expression()
                val = self.visit(ast)
                result.append(str(val))
        return ''.join(result)

    def visit_Identifier(self, node):
        return self.env.get(node.name)

    def visit_Boolean(self, node):
        return node.value

    def visit_Null(self, node):
        return NULL_VALUE

    def visit_BinaryOp(self, node):
        if node.op == 'and':
            left = self.visit(node.left)
            if not self.is_truthy(left):
                return left
            return self.visit(node.right)
        if node.op == 'or':
            left = self.visit(node.left)
            if self.is_truthy(left):
                return left
            return self.visit(node.right)

        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            if right == 0:
                self.error("除零错误", node)
            return left / right
        elif node.op == '//':
            if right == 0:
                self.error("除零错误", node)
            return left // right
        elif node.op == '%':
            if right == 0:
                self.error("取余除零错误", node)
            return left % right
        elif node.op == '**':
            return left ** right
        elif node.op == '==':
            return left is right if left is NULL_VALUE or right is NULL_VALUE else left == right
        elif node.op == '!=':
            return left is not right if left is NULL_VALUE or right is NULL_VALUE else left != right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        elif node.op == 'in':
            if isinstance(right, MeowList):
                return right.contains(left)
            if isinstance(right, str):
                return str(left) in right
            if isinstance(right, (list, tuple)):
                return left in right
            return False
        elif node.op == 'not in':
            if isinstance(right, MeowList):
                return not right.contains(left)
            if isinstance(right, str):
                return str(left) not in right
            return left not in right
        elif node.op == '++':
            if isinstance(left, MeowList) and isinstance(right, MeowList):
                return MeowList(left.items + right.items)
            return str(left) + str(right)
        elif node.op == '--':
            if isinstance(left, MeowList) and isinstance(right, MeowList):
                return MeowList([x for x in left.items if x not in right.items])
            return set(left) - set(right)
        elif node.op == '--/':
            if isinstance(left, MeowList) and isinstance(right, MeowList):
                left_set = set(left.items)
                right_set = set(right.items)
                sym_diff = left_set.symmetric_difference(right_set)
                return MeowList(list(sym_diff))
            return left ^ right
        elif node.op == '&&':
            if isinstance(left, MeowList) and isinstance(right, MeowList):
                return MeowList([x for x in left.items if x in right.items])
            return set(left) & set(right)
        else:
            self.error(f"不支持的操作: {node.op}", node)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if node.op == '-':
            return -operand
        elif node.op == 'not':
            return not operand
        self.error(f"不支持的单目操作: {node.op}", node)

    def visit_Assignment(self, node):
        value = self.visit(node.value)
        target = node.target

        if isinstance(target, Identifier):
            if self.env.has(target.name):
                self.env.set(target.name, value)
            else:
                self.env.define(target.name, value)
        elif isinstance(target, Property):
            obj = self.visit(target.obj)
            if isinstance(obj, MeowInstance):
                obj.set(target.name, value)
            else:
                self.error(f"无法设置属性: {target.name}", node)
        elif isinstance(target, Index):
            obj = self.visit(target.obj)
            index = self.visit(target.index)
            if isinstance(obj, MeowList):
                obj.set(index, value)
            elif isinstance(obj, MeowDict):
                obj.set(index, value)
            else:
                self.error(f"无法设置索引: {type(obj)}", node)
        else:
            self.error(f"不支持的赋值目标: {type(target).__name__}", node)

        return value

    def visit_AugmentedAssign(self, node):
        current = self.visit(node.target)
        value = self.visit(node.value)
        op = node.op
        if op == '+=':
            result = current + value
        elif op == '-=':
            result = current - value
        elif op == '*=':
            result = current * value
        elif op == '/=':
            result = current / value
        else:
            self.error(f"不支持的复合赋值: {op}", node)
        self.env.set(node.target.name, result)
        return result

    def visit_FunctionCall(self, node):
        callee = self.visit(node.callee)
        args = [self.visit(arg) for arg in node.args]

        if isinstance(callee, MeowFunction):
            result = callee.call(self, args)
            return result if result is not None else NULL_VALUE
        elif isinstance(callee, MeowLambda):
            result = callee.call(self, args)
            return result if result is not None else NULL_VALUE
        elif isinstance(callee, MeowClass):
            return callee.instantiate(self, args)
        elif callable(callee):
            result = callee(*args)
            return result if result is not None else NULL_VALUE
        else:
            self.error(f"无法调用: {callee} (类型: {type(callee).__name__})", node)

    def visit_FunctionDef(self, node):
        func = MeowFunction(node.name, node.params, node.body, self.env)
        self.env.define(node.name, func)
        return NULL_VALUE

    def visit_Return(self, node):
        if node.value is not None:
            value = self.visit(node.value)
            raise MeowReturn(value)
        raise MeowReturn(NULL_VALUE)

    def visit_Lambda(self, node):
        return MeowLambda(node.params, node.body, self.env)

    def visit_If(self, node):
        cond = self.is_truthy(self.visit(node.condition))
        if cond:
            return self.visit(node.then_block)
        for elif_clause in node.elif_clauses:
            if self.is_truthy(self.visit(elif_clause.condition)):
                return self.visit(elif_clause.block)
        if node.else_block is not None:
            return self.visit(node.else_block)
        return NULL_VALUE

    def is_truthy(self, value):
        if value is NULL_VALUE:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value != ''
        if isinstance(value, MeowList):
            return value.length() > 0
        return True

    def visit_For(self, node):
        iterable = self.visit(node.iterable)
        result = NULL_VALUE
        if isinstance(iterable, MeowList):
            items = iterable.items
        elif isinstance(iterable, range):
            items = list(iterable)
        elif isinstance(iterable, (list, tuple)):
            items = iterable
        elif hasattr(iterable, '__iter__'):
            items = list(iterable)
        else:
            items = [iterable]

        for item in items:
            env = Environment(self.env)
            old_env = self.env
            self.env = env
            self.env.define(node.var.name, item)
            try:
                r = self.visit(node.body)
                result = r
            except MeowReturn as e:
                return e
            except MeowBreak:
                break
            except MeowContinue:
                continue
            finally:
                self.env = old_env
        return result

    def visit_While(self, node):
        result = NULL_VALUE
        while self.is_truthy(self.visit(node.condition)):
            try:
                r = self.visit(node.body)
                result = r
            except MeowReturn as e:
                return e
            except MeowBreak:
                break
            except MeowContinue:
                continue
        return result

    def visit_Break(self, node):
        raise MeowBreak()

    def visit_Continue(self, node):
        raise MeowContinue()

    def visit_ListLiteral(self, node):
        values = [self.visit(elem) for elem in node.elements]
        return MeowList(values)

    def visit_DictLiteral(self, node):
        entries = []
        for entry in node.entries:
            key = self.visit(entry.key)
            value = self.visit(entry.value)
            entries.append((key, value))
        return MeowDict(entries)

    def visit_Index(self, node):
        obj = self.visit(node.obj)
        index = self.visit(node.index)
        if isinstance(obj, MeowList):
            return obj.get(index)
        if isinstance(obj, MeowDict):
            return obj.get(index)
        if isinstance(obj, str):
            return obj[index - 1] if index > 0 else obj[len(obj) + index]
        if isinstance(obj, (list, tuple)):
            return obj[index - 1] if index > 0 else obj[len(obj) + index]
        self.error(f"不支持索引操作的类型: {type(obj)}", node)

    def visit_ListComp(self, node):
        iterable = self.visit(node.iterable)
        results = []
        if isinstance(iterable, MeowList):
            items = iterable.items
        elif isinstance(iterable, (list, tuple, range)):
            items = list(iterable)
        else:
            items = [iterable]

        for item in items:
            env = Environment(self.env)
            old_env = self.env
            self.env = env
            self.env.define(node.var.name, item)
            try:
                val = self.visit(node.expr)
                results.append(val)
            finally:
                self.env = old_env
        return MeowList(results)

    def visit_Property(self, node):
        obj = self.visit(node.obj)
        if isinstance(obj, MeowInstance):
            val = obj.get(node.name)
            if isinstance(val, MeowFunction):
                def bound_method(*args):
                    return val.call(self, [obj] + list(args))
                return bound_method
            return val
        if isinstance(obj, MeowList):
            if node.name.isdigit():
                return obj.items[int(node.name)]
            if node.name == 'length':
                return obj.length()
            if node.name == 'add':
                def add_method(item):
                    obj.add(item)
                    return NULL_VALUE
                return add_method
            if node.name == 'pop':
                def pop_method(index=-1):
                    return obj.pop(index)
                return pop_method
            if node.name == 'remove':
                def remove_method(item):
                    return obj.remove(item)
                return remove_method
            if node.name == 'contains':
                def contains_method(item):
                    return obj.contains(item)
                return contains_method
        if isinstance(obj, MeowDict):
            if node.name in obj.data:
                return obj.data[node.name]
            if node.name == 'keys':
                return obj.keys()
            if node.name == 'length':
                return obj.length()
            if node.name == 'set':
                def dict_set_method(key, value):
                    obj.set(key, value)
                    return NULL_VALUE
                return dict_set_method
        if isinstance(obj, str):
            if node.name == 'length':
                return len(obj)
            if node.name == 'up':
                return obj.upper()
            if node.name == 'low':
                return obj.lower()
            if node.name == 'strip':
                return obj.strip()
            if node.name == 'replace':
                def replace_method(old, new):
                    return obj.replace(old, new)
                return replace_method
            if node.name == 'split':
                def split_method(sep=None):
                    if sep is None:
                        return MeowList(obj.split())
                    return MeowList(obj.split(sep))
                return split_method
            if node.name == 'contains':
                def contains_method(sub):
                    return sub in obj
                return contains_method
        self.error(f"对象没有属性: {node.name}", node)

    def visit_ClassDef(self, node):
        methods = {}
        base_class = None
        if node.base_class:
            base_class = self.visit(node.base_class)
            if not isinstance(base_class, MeowClass):
                self.error(f"基类必须是类: {type(base_class)}", node)

        for method in node.body:
            func = MeowFunction(
                method.name, method.params, method.body, self.env,
                is_method=True
            )
            methods[method.name] = func

        if base_class:
            for name, method in base_class.methods.items():
                if name not in methods:
                    methods[name] = method

        cls = MeowClass(node.name, base_class, methods)
        self.env.define(node.name, cls)
        return NULL_VALUE

    def visit_Try(self, node):
        try:
            return self.visit(node.try_block)
        except (MeowException, MeowRuntimeError) as exc:
            if isinstance(exc, MeowRuntimeError):
                exc = MeowException('RuntimeError', exc.message)
            if node.except_var:
                env = Environment(self.env)
                old_env = self.env
                self.env = env
                self.env.define(node.except_var.name, exc)
                try:
                    result = self.visit(node.except_block)
                    return result
                finally:
                    self.env = old_env
            elif node.except_block:
                return self.visit(node.except_block)
            else:
                raise
        except MeowReturn:
            raise
        except MeowBreak:
            raise
        except MeowContinue:
            raise
        finally:
            if node.finally_block:
                self.visit(node.finally_block)

    def visit_Raise(self, node):
        message = self.visit(node.message) if node.message else ''
        raise MeowException(node.exc_name, message)

    def visit_ErrorDef(self, node):
        self.error_classes[node.name] = node.message
        return NULL_VALUE

    def visit_Import(self, node):
        from .lexer import Lexer as MeowLexer
        from .parser import Parser as MeowParser
        meow_code = '\n'.join(node.names) if isinstance(node.names, list) else ''
        lexer = MeowLexer(meow_code)
        tokens = lexer.tokenize()
        parser = MeowParser(tokens)
        ast = parser.parse()
        return self.visit(ast)

    def visit_CrossLangBlock(self, node):
        result = self.cross_lang.execute(node.lang, node.body, self.env)
        if isinstance(result, dict):
            for key, value in result.items():
                self.env.define(key, value)
        return result
