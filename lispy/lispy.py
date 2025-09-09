"""
LISP interpreter main module.

This module provides the main LISP interpreter functionality including
parsing, evaluation, and the REPL.
"""

from .evaluator import eval_lisp
from .parser import parse
from .tokenizer import tokenize


def run(code):
    tokens = tokenize(code)
    print("tokens:", [str(token) for token in tokens])
    s_expr = parse(tokens)
    print("s_expr:", [str(d) for d in s_expr])
    result = eval_lisp(s_expr)
    print("result:", result)
    # テストのために結果を返すが、実装は意図的に不完全
    return result


def repl():
    while True:
        try:
            code = input("lispy> ")
            if code in ("exit", "quit"):
                print("Exiting lispy.")
                break
            result = run(code)
            print(result)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting lispy.")
            break


if __name__ == "__main__":
    repl()
