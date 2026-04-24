class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise NameError(f"未定义的变量: {name}")

    def set(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value)
            return
        raise NameError(f"未定义的变量: {name}")

    def has(self, name):
        if name in self.values:
            return True
        if self.parent is not None:
            return self.parent.has(name)
        return False

    def __repr__(self):
        return f"Environment({self.values})"


class MeowReturn(Exception):
    def __init__(self, value):
        self.value = value


class MeowBreak(Exception):
    pass


class MeowContinue(Exception):
    pass


class MeowException(BaseException):
    def __init__(self, exc_name, message):
        self.exc_name = exc_name
        self.message = message

    def __str__(self):
        return f"{self.exc_name}: {self.message}"


class MeowFunction:
    def __init__(self, name, params, body, closure, is_method=False):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure
        self.is_method = is_method

    def call(self, interpreter, args):
        env = Environment(self.closure)
        for i, param in enumerate(self.params):
            param_name = param.name if hasattr(param, 'name') else param
            if i < len(args):
                env.define(param_name, args[i])
            else:
                env.define(param_name, None)
        if self.is_method:
            env.define('self', args[0] if args else None)
        old_env = interpreter.env
        interpreter.env = env
        try:
            interpreter.visit(self.body)
            return None
        except MeowReturn as ret:
            return ret.value
        finally:
            interpreter.env = old_env

    def __repr__(self):
        return f"<MeowFunction {self.name}>"


class MeowLambda:
    def __init__(self, params, body, closure):
        self.params = params
        self.body = body
        self.closure = closure

    def call(self, interpreter, args):
        env = Environment(self.closure)
        for i, param in enumerate(self.params):
            param_name = param.name if hasattr(param, 'name') else param
            if i < len(args):
                env.define(param_name, args[i])
            else:
                env.define(param_name, None)
        old_env = interpreter.env
        interpreter.env = env
        try:
            return interpreter.visit(self.body)
        except MeowReturn as ret:
            return ret.value
        finally:
            interpreter.env = old_env

    def __repr__(self):
        return f"<MeowLambda>"


class MeowClass:
    def __init__(self, name, base_class, methods):
        self.name = name
        self.base_class = base_class
        self.methods = methods

    def instantiate(self, interpreter, args):
        instance = MeowInstance(self)
        init_method = self.find_method('init')
        if init_method:
            init_method.call(interpreter, [instance] + args)
        return instance

    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.base_class:
            return self.base_class.find_method(name)
        return None

    def __repr__(self):
        return f"<MeowClass {self.name}>"


class MeowInstance:
    def __init__(self, cls):
        self.cls = cls
        self.properties = {}

    def get(self, name):
        if name in self.properties:
            return self.properties[name]
        method = self.cls.find_method(name)
        if method:
            return method
        raise NameError(f"实例没有属性: {name}")

    def set(self, name, value):
        self.properties[name] = value

    def __repr__(self):
        return f"<MeowInstance of {self.cls.name}>"


class MeowList:
    def __init__(self, items=None):
        self.items = items or []

    def add(self, item):
        self.items.append(item)

    def pop(self, index=-1):
        if not self.items:
            return None
        if isinstance(index, int) and index < 0:
            idx = len(self.items) + index
            if idx < 0:
                return None
            return self.items.pop(idx)
        if isinstance(index, int) and index > 0:
            idx = index - 1
            if idx >= len(self.items):
                return None
            return self.items.pop(idx)
        return self.items.pop()

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def length(self):
        return len(self.items)

    def get(self, index):
        if isinstance(index, int) and index > 0:
            idx = index - 1
            if 0 <= idx < len(self.items):
                return self.items[idx]
            raise IndexError(f"索引 {index} 超出范围，列表长度 {len(self.items)}")
        if isinstance(index, int) and index < 0:
            idx = len(self.items) + index
            if 0 <= idx < len(self.items):
                return self.items[idx]
            raise IndexError(f"索引 {index} 超出范围，列表长度 {len(self.items)}")
        if index == 0:
            raise IndexError("Meow 索引从 1 开始")
        raise IndexError(f"无效索引: {index}")

    def set_item(self, index, value):
        if isinstance(index, int) and index > 0:
            idx = index - 1
            if 0 <= idx < len(self.items):
                self.items[idx] = value
                return
            raise IndexError(f"索引 {index} 超出范围")
        if isinstance(index, int) and index < 0:
            idx = len(self.items) + index
            if 0 <= idx < len(self.items):
                self.items[idx] = value
                return
            raise IndexError(f"索引 {index} 超出范围")
        raise IndexError(f"无效索引: {index}")

    def to_list(self):
        return self.items

    def contains(self, item):
        return item in self.items

    def __repr__(self):
        return f"[{', '.join(repr(i) for i in self.items)}]"


class MeowDict:
    def __init__(self, entries=None):
        self.data = {}
        if entries:
            for k, v in entries:
                self.data[k] = v

    def get(self, key):
        if key in self.data:
            return self.data[key]
        return None

    def set(self, key, value):
        self.data[key] = value

    def length(self):
        return len(self.data)

    def keys(self):
        return MeowList(list(self.data.keys()))

    def __repr__(self):
        items = ', '.join(f"{k!r}: {v!r}" for k, v in self.data.items())
        return f"{{{items}}}"


NULL_VALUE = object()
