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


def meow_int(val):
    if isinstance(val, str):
        try:
            if val.startswith('0x') or val.startswith('0X'):
                return int(val, 16)
            if val.startswith('0b') or val.startswith('0B'):
                return int(val, 2)
            return int(val)
        except ValueError:
            raise RuntimeError(f"无法将 '{val}' 转换为整数")
    if isinstance(val, float):
        return int(val)
    if isinstance(val, int):
        return val
    raise RuntimeError(f"无法将 {type(val).__name__} 转换为整数")


def meow_float(val):
    if isinstance(val, str):
        try:
            return float(val)
        except ValueError:
            raise RuntimeError(f"无法将 '{val}' 转换为浮点数")
    if isinstance(val, int):
        return float(val)
    if isinstance(val, float):
        return val
    raise RuntimeError(f"无法将 {type(val).__name__} 转换为浮点数")


def register_builtins(env):
    env.define('print', meow_print)
    env.define('len', meow_len)
    env.define('type', meow_type)
    env.define('input', meow_input)
    env.define('range', meow_range)
    env.define('int', meow_int)
    env.define('float', meow_float)
