import sys
import io

from .utils import MeowError


class CrossLangBridge:
    def __init__(self):
        self.shared_vars = {}

    def execute(self, lang, code, env):
        if lang == 'python':
            return self._exec_python(code, env)
        if lang == 'shell':
            return self._exec_shell(code, env)
        raise MeowError(f"不支持的跨语言目标: {lang}")

    def _exec_python(self, code, env):
        local_scope = {}
        local_scope.update(self.shared_vars)

        try:
            compiled = compile(code, '<cross_lang>', 'exec')
            exec(compiled, local_scope)
        except Exception as e:
            raise MeowError(f"跨语言 Python 执行错误: {e}")

        imported_vars = {}
        for key, value in local_scope.items():
            if key.startswith('_'):
                continue
            if key not in self.shared_vars or self.shared_vars[key] is not value:
                imported_vars[key] = value

        return imported_vars

    def share_variable(self, name, value):
        self.shared_vars[name] = value

    def get_shared(self, name):
        return self.shared_vars.get(name, None)
