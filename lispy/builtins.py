import math
from functools import reduce

# 演算子
OPERATORS = {
    '+': lambda *args: sum(args),
    '-': lambda a, b=None: -a if b is None else a - b,
    '*': lambda *args: reduce(lambda x, y: x * y, args, 1),
    '/': lambda a, b: a / b,
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
