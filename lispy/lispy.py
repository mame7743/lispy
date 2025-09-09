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

    # 各式を評価
    results = []
    for expr in s_expr:
        result = eval_lisp(expr)
        results.append(result)

    print("result:", results)
    return results


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
