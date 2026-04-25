import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .utils import MeowError, MeowRuntimeError
from .environment import NULL_VALUE


def run_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"错误: 文件未找到: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取文件失败: {e}")
        sys.exit(1)

    run_source(source, filepath)


def run_source(source, filename='<stdin>'):
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
    except MeowError as e:
        print(f"语法错误 ({filename}): {e}")
        sys.exit(1)
    except MeowRuntimeError as e:
        print(f"运行时错误 ({filename}): {e}")
        if os.environ.get('MEOW_DEBUG'):
            traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"内部错误 ({filename}): {e}")
        if os.environ.get('MEOW_DEBUG'):
            traceback.print_exc()
        sys.exit(1)


def run_repl():
    print("Meow 语言 REPL (输入 'exit' 退出)")
    interpreter = Interpreter()

    while True:
        try:
            line = input('>>> ')
            if line.strip() == 'exit':
                break
            if line.strip() == '':
                continue

            tokens = Lexer(line).tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            result = interpreter.interpret(ast)
            if result is not None and result is not NULL_VALUE:
                print(repr(result))

        except MeowError as e:
            print(f"语法错误: {e}")
        except MeowRuntimeError as e:
            print(f"运行时错误: {e}")
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")


def main():
    if len(sys.argv) < 2:
        run_repl()
        return

    filepath = sys.argv[1]
    run_file(filepath)


if __name__ == '__main__':
    main()
