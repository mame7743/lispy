"""
LISP interpreter main module.

This module provides the main LISP interpreter functionality including
parsing, evaluation, and the REPL.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from .evaluator import eval_lisp
from .parser import parse
from .tokenizer import tokenize

__version__ = "0.1.0"


def run(code, debug=False):
    """コードを実行する"""
    tokens = tokenize(code)
    if debug:
        print("tokens:", [str(token) for token in tokens])

    s_expr: list[Any] = parse(tokens)
    if debug:
        print("s_expr:", [str(d) for d in s_expr])

    # 各式を評価
    results = []
    for expr in s_expr:
        if debug:
            print(f"評価中: {expr}")
        result = eval_lisp(expr)
        if debug:
            print(f"評価結果: {result}")
        results.append(result)

    if len(results) == 1:
        return results[0]
    else:
        return '(' + ' '.join(str(r) for r in results) + ')'


def run_file(filename, debug=False):
    """ファイルを実行する"""
    try:
        file_path = Path(filename)
        if not file_path.exists():
            print(f"エラー: ファイル '{filename}' が見つかりません。", file=sys.stderr)
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        if debug:
            print(f"ファイル '{filename}' の内容:")
            print("--- ファイル開始 ---")
            print(code)
            print("--- ファイル終了 ---")
        else:
            print(f"ファイル '{filename}' を実行中...")

        return run(code, debug)
    except Exception as e:
        print(f"ファイル実行エラー: {e}", file=sys.stderr)
        return None


def repl():
    """対話式REPL"""
    session = PromptSession(history=FileHistory(".history"))
    print("LISPY REPL - 'exit' または 'quit' で終了")
    while True:
        try:
            code = session.prompt("lispy > ")
            if code in ("exit", "quit"):
                print("Exiting lispy.")
                break
            if code.strip():
                result = run(code)
                print(result)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting lispy.")
            break


def main():


    """メイン関数 - コマンドライン引数を処理"""
    parser = argparse.ArgumentParser(
        description='LISPY - Simple LISP Interpreter',
        prog='lispy'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'lispy {__version__}'
    )

    parser.add_argument(
        '--file', '-f',
        type=str,
        help='LISPファイルを実行'
    )

    parser.add_argument(
        '--eval', '-e',
        type=str,
        help='コードを直接実行'
    )

    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='詳細なデバッグ情報を表示する'
    )

    args = parser.parse_args()

    # ファイル実行モード
    if args.file:
        result = run_file(args.file, args.debug)
        if result is None:
            sys.exit(1)
        print("実行完了")
        return

    # コード直接実行モード
    if args.eval:
        try:
            result = run(args.eval, args.debug)
        except Exception as e:
            print(f"実行エラー: {e}", file=sys.stderr)
            sys.exit(1)
        return    # デフォルト: REPLモード
    repl()


if __name__ == "__main__":
    main()
