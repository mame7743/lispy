"""
LISPインタープリターのエバリューターモジュール

S式を環境下で評価して結果を返す
"""

from typing import Any, Dict, Optional

from .builtins import BUILTINS, OPERATORS


class Environment:
    """LISP評価環境"""

    def __init__(self, parent=None):
        self.bindings: Dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any):
        """変数を定義"""
        self.bindings[name] = value

    def lookup(self, name: str) -> Any:
        """変数を検索"""
        if name in self.bindings:
            return self.bindings[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Undefined variable: {name}")


def create_global_env() -> Environment:
    """グローバル環境を作成"""
    env = Environment()
    # 演算子を定義
    for name, func in OPERATORS.items():
        env.define(name, func)
    # 組み込み関数を定義
    for name, func in BUILTINS.items():
        env.define(name, func)
    return env


def eval_lisp(expr: Any, env: Optional[Environment] = None) -> Any:
    """S式を環境下で評価"""
    if env is None:
        env = create_global_env()

    # 数値リテラル
    if isinstance(expr, (int, float)):
        return expr

    # 文字列リテラル（タプルで表現）
    if (isinstance(expr, tuple) and len(expr) == 2 and
            expr[0] == 'STRING_LITERAL'):
        return expr[1]

    # シンボル（変数参照）
    if isinstance(expr, str):
        return env.lookup(expr)

    # リスト（関数呼び出しまたは特殊形式）
    if isinstance(expr, list):
        if not expr:
            return expr

        # 特殊形式の処理
        if expr[0] == 'if':
            # (if condition then-expr else-expr)
            if len(expr) != 4:
                raise ValueError("if式は4つの要素が必要です: (if condition then else)")
            condition = eval_lisp(expr[1], env)
            if condition:
                return eval_lisp(expr[2], env)
            else:
                return eval_lisp(expr[3], env)

        # 通常の関数呼び出し
        func = eval_lisp(expr[0], env)

        # 残りの要素が引数
        args = [eval_lisp(arg, env) for arg in expr[1:]]
        # 関数呼び出し
        if callable(func):
            return func(*args)
        else:
            raise TypeError(f"{func} は呼び出し可能ではありません")
