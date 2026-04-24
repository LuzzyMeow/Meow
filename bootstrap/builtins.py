from .environment import (
    Environment, NULL_VALUE, MeowFunction, MeowLambda, MeowList,
    MeowReturn, MeowBreak, MeowContinue,
)


def meow_print(*args):
    output = ' '.join('null' if a is NULL_VALUE else str(a) for a in args)
    print(output)
    return NULL_VALUE


def meow_len(obj):
    if isinstance(obj, MeowList):
        return obj.length()
    if hasattr(obj, '__len__'):
        return len(obj)
    return 0


def meow_type(obj):
    if obj is NULL_VALUE:
        return 'null'
    if isinstance(obj, bool):
        return 'bool'
    if isinstance(obj, (int, float)):
        return 'number'
    if isinstance(obj, str):
        return 'string'
    if isinstance(obj, MeowList):
        return 'list'
    if isinstance(obj, MeowFunction):
        return 'function'
    if isinstance(obj, MeowLambda):
        return 'lambda'
    return type(obj).__name__


def meow_input(prompt=''):
    return input(prompt)


def meow_range(start, end=None, step=1):
    if end is None:
        return MeowList(list(range(1, start + 1)))
    return MeowList(list(range(start, end + 1, step)))


def register_builtins(env):
    env.define('print', meow_print)
    env.define('len', meow_len)
    env.define('type', meow_type)
    env.define('input', meow_input)
    env.define('range', meow_range)
