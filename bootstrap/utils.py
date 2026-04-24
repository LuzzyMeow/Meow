class MeowError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self._format())

    def _format(self):
        parts = ["MeowError"]
        if self.line is not None:
            parts.append(f" at line {self.line}")
            if self.column is not None:
                parts.append(f", column {self.column}")
        parts.append(f": {self.message}")
        return "".join(parts)


class MeowRuntimeError(Exception):
    def __init__(self, message, line=None):
        self.message = message
        self.line = line
        super().__init__(self._format())

    def _format(self):
        parts = ["RuntimeError"]
        if self.line is not None:
            parts.append(f" at line {self.line}")
        parts.append(f": {self.message}")
        return "".join(parts)
