import math
import re
from functools import reduce
from operator import le


def operator_add(*args):
    return sum(args)


def operator_mul(*args):

    if len(args) == 0:
        return 1

    if len(args) == 1:
        return args[0]

    result = args[0]
    for x in args[1:]:
        result *= x
    return result


def operator_sub(*args):
    if len(args) == 0:
        raise ValueError("'-'演算子には少なくとも1つの引数が必要です")

    if len(args) == 1:
        return -args[0]

    return args[0] - sum(args[1:])


def operator_div(*args):

    if len(args) == 0:
        raise ValueError("'/'演算子には少なくとも1つの引数が必要です")

    if len(args) == 1:
        return 1 / args[0]

    result = args[0]
    for b in args[1:]:
        result /= b
    return result


# 演算子
OPERATORS = {
    '+': operator_add,
    '-': operator_sub,
    '*': operator_mul,
    '/': operator_div,
    '%': lambda a, b: a % b,
    '=': lambda a, b: a == b,
    '<': lambda a, b: a < b,
    '>': lambda a, b: a > b,
    '<=': lambda a, b: a <= b,
    '>=': lambda a, b: a >= b,
}

# 組み込み関数
BUILTINS = {
    'sin': math.sin,
    'cos': math.cos,
    'sqrt': math.sqrt,
    'print': lambda x: print(x) or x,  # printして値を返す
    'str': str,  # 文字列変換
    'concat': lambda *args: ''.join(str(arg) for arg in args),  # 文字列結合
    'range': lambda start, end=None: (
        list(range(start, end) if end is not None else range(start))
    ),
    'length': len,
    'map': lambda func, lst: [func(x) for x in lst],
    'filter': lambda func, lst: [x for x in lst if func(x)],
    'list': lambda *args: list(args),
    'and': lambda a, b: a and b,
    'or': lambda a, b: a or b,
    'not': lambda x: not x,
}
