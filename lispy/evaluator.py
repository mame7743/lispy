"""
LISPインタープリターのエバリューターモジュール

S式を環境下で評価して結果を返す
"""

from functools import reduce
from typing import Any, Dict, Optional


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


def operator_add(*args):
    return sum(args)


def operator_sub(*args):
    if len(args) == 0:
        raise ValueError("Subtraction requires at least one argument")
    elif len(args) == 1:
        return -args[0]
    else:
        return args[0] - sum(args[1:])


def operator_mul(*args):
    return reduce(lambda x, y: x * y, args, 1)


def operator_div(*args):
    if len(args) == 0:
        raise ValueError("Division requires at least one argument")
    elif len(args) == 1:
        return 1 / args[0]
    else:
        return reduce(lambda x, y: x / y, args)


def create_global_env() -> Environment:
    """グローバル環境を作成"""
    env = Environment()

    # 基本的な算術演算子を定義
    env.define("+", operator_add)
    env.define("-", operator_sub)
    env.define("*", operator_mul)
    env.define("/", operator_div)

    return env


def eval_lisp(expr: Any, env: Optional[Environment] = None) -> Any:
    """S式を環境下で評価"""
    if env is None:
        env = create_global_env()

    # 数値リテラル
    if isinstance(expr, (int, float)):
        return expr

    # シンボル（変数参照）
    if isinstance(expr, str):
        return env.lookup(expr)

    # リスト（関数呼び出し）
    if isinstance(expr, list):
        if not expr:
            return expr

        # 最初の要素が関数
        func = eval_lisp(expr[0], env)

        # 残りの要素が引数
        args = [eval_lisp(arg, env) for arg in expr[1:]]

        # 関数を適用
        if callable(func):
            return func(*args)
        else:
            raise TypeError(f"'{expr[0]}' is not callable")

    # その他の型はそのまま返す
    return expr
