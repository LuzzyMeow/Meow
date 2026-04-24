class Node:
    pass


class Program(Node):
    def __init__(self, statements):
        self.statements = statements


class Block(Node):
    def __init__(self, statements):
        self.statements = statements


class Number(Node):
    def __init__(self, value, line=None):
        self.value = value
        self.line = line


class String(Node):
    def __init__(self, value, line=None):
        self.value = value
        self.line = line


class StringInterp(Node):
    def __init__(self, parts, line=None):
        self.parts = parts
        self.line = line


class Identifier(Node):
    def __init__(self, name, line=None):
        self.name = name
        self.line = line


class Boolean(Node):
    def __init__(self, value, line=None):
        self.value = value
        self.line = line


class Null(Node):
    def __init__(self, line=None):
        self.line = line


class BinaryOp(Node):
    def __init__(self, left, op, right, line=None):
        self.left = left
        self.op = op
        self.right = right
        self.line = line


class UnaryOp(Node):
    def __init__(self, op, operand, line=None):
        self.op = op
        self.operand = operand
        self.line = line


class Assignment(Node):
    def __init__(self, target, value, line=None):
        self.target = target
        self.value = value
        self.line = line


class AugmentedAssign(Node):
    def __init__(self, target, op, value, line=None):
        self.target = target
        self.op = op
        self.value = value
        self.line = line


class FunctionCall(Node):
    def __init__(self, callee, args, line=None):
        self.callee = callee
        self.args = args
        self.line = line


class FunctionDef(Node):
    def __init__(self, name, params, body, line=None):
        self.name = name
        self.params = params
        self.body = body
        self.line = line


class Return(Node):
    def __init__(self, value, line=None):
        self.value = value
        self.line = line


class Lambda(Node):
    def __init__(self, params, body, line=None):
        self.params = params
        self.body = body
        self.line = line


class If(Node):
    def __init__(self, condition, then_block, elif_clauses=None, else_block=None, line=None):
        self.condition = condition
        self.then_block = then_block
        self.elif_clauses = elif_clauses or []
        self.else_block = else_block
        self.line = line


class ElifClause(Node):
    def __init__(self, condition, block, line=None):
        self.condition = condition
        self.block = block
        self.line = line


class For(Node):
    def __init__(self, var, iterable, body, line=None):
        self.var = var
        self.iterable = iterable
        self.body = body
        self.line = line


class While(Node):
    def __init__(self, condition, body, line=None):
        self.condition = condition
        self.body = body
        self.line = line


class Break(Node):
    def __init__(self, line=None):
        self.line = line


class Continue(Node):
    def __init__(self, line=None):
        self.line = line


class ListLiteral(Node):
    def __init__(self, elements, line=None):
        self.elements = elements
        self.line = line


class DictLiteral(Node):
    def __init__(self, entries, line=None):
        self.entries = entries
        self.line = line


class DictEntry(Node):
    def __init__(self, key, value, line=None):
        self.key = key
        self.value = value
        self.line = line


class Index(Node):
    def __init__(self, obj, index, line=None):
        self.obj = obj
        self.index = index
        self.line = line


class ListComp(Node):
    def __init__(self, expr, var, iterable, line=None):
        self.expr = expr
        self.var = var
        self.iterable = iterable
        self.line = line


class Property(Node):
    def __init__(self, obj, name, line=None):
        self.obj = obj
        self.name = name
        self.line = line


class ClassDef(Node):
    def __init__(self, name, base_class=None, body=None, line=None):
        self.name = name
        self.base_class = base_class
        self.body = body or []
        self.line = line


class Try(Node):
    def __init__(self, try_block, except_var, except_block, finally_block, line=None):
        self.try_block = try_block
        self.except_var = except_var
        self.except_block = except_block
        self.finally_block = finally_block
        self.line = line


class Raise(Node):
    def __init__(self, exc_name, message, line=None):
        self.exc_name = exc_name
        self.message = message
        self.line = line


class ErrorDef(Node):
    def __init__(self, name, message, line=None):
        self.name = name
        self.message = message
        self.line = line


class Import(Node):
    def __init__(self, module, names, line=None):
        self.module = module
        self.names = names
        self.line = line


class CrossLangBlock(Node):
    def __init__(self, lang, body, line=None):
        self.lang = lang
        self.body = body
        self.line = line
