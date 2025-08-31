import re
from dataclasses import dataclass
from enum import Enum
from token import OP
from typing import Union


class TokenKind(Enum):
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    INTEGER = "INTEGER"
    OPERATOR = "OPERATOR"
    SYMBOL = "SYMBOL"

@dataclass
class Token:
    kind: TokenKind
    value: str

    def __str__(self):
        return f"Token(\'{self.kind.value}\', \'{self.value}\')"


class OperatorKind(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"

class Operator:
    kind: OperatorKind

    def exec(self, arg: Object):
        match self.kind:
            case OperatorKind.ADD:
                return self.add(arg)
            case OperatorKind.SUB:
                return self.sub(arg)
            case OperatorKind.MUL:
                return self.mul(arg)
            case OperatorKind.DIV:
                return self.div(arg)
            case _:
                raise RuntimeError(f"Unknown operator: {self.kind}")


    def add(self, obj: Object):
        sum = 0
        while obj.kind != ObjectKind.NIL:
            match obj.kind:
                case ObjectKind.INTEGER:
                    sum += obj.value
                case _:
                    break
        return sum

    def sub(self, obj: Object):
        match obj.kind:
            case ObjectKind.INTEGER:
                return self.value - obj.value
            case _:
                raise RuntimeError(f"Invalid operand for -: {obj}")

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        return a / b

class ObjectKind(Enum):
    INTEGER = "INTEGER"
    SYMBOL = "SYMBOL"
    OPERATOR = "OPERATOR"
    CONS = "CONS"
    NIL = "NIL"

@dataclass
class Cons:
    car: 'Object'
    cdr: 'Object'

    def __str__(self):
        return f"Cons(car={self.car}, cdr={self.cdr})"


@dataclass
class Object:
    kind: ObjectKind
    value: Union[int, str, Cons, Operator, None]



def tokenize(code : str) -> list[Token]:

    token_spec = {
        "LPAREN":     r"\(",
        "RPAREN":     r"\)",
        "INTEGER":    r"[0-9]+",
        "OPERATOR":   r"[+\-*/]",
        "SYMBOL":     r"[a-zA-Z_][a-zA-Z0-9_]*",
        "WHITESPACE": r"\s+",
        "NEWLINE":    r"\n",
        "MISMATCH":   r".",
    }

    tok_regex = "|".join(f"(?P<{name}>{pattern})"
                         for name, pattern in token_spec.items())
    get_token = re.compile(tok_regex).finditer
    tokens = []

    for m in get_token(code):
        kind = m.lastgroup
        value = m.group()

        match kind:
            case "LPAREN":
                tokens.append(Token(TokenKind.LPAREN, value))
            case "RPAREN":
                tokens.append(Token(TokenKind.RPAREN, value))
            case "INTEGER":
                tokens.append(Token(TokenKind.INTEGER, value))
            case "OPERATOR":
                tokens.append(Token(TokenKind.OPERATOR, value))
            case "SYMBOL":
                tokens.append(Token(TokenKind.SYMBOL, value))
            case "WHITESPACE" | "NEWLINE":
                continue
            case "MISMATCH":
                raise RuntimeError(f"Unexpected character: {value}")
            case _:
                raise RuntimeError(f"Unknown token kind: {kind}")

    return tokens


def parse(tokens):
    # ここにLISPのパースロジックを実装します
    if len(tokens) == 0:
        return None

    token = tokens[0]
    tokens = tokens[1:]

    match token.kind:
        case TokenKind.LPAREN:
            return parse(tokens)
        case TokenKind.RPAREN:
            return Object(ObjectKind.NIL, None)
        case TokenKind.INTEGER:
            car = Object(ObjectKind.INTEGER, int(token.value))
            cdr = parse(tokens)
            return Object(ObjectKind.CONS, Cons(car, cdr))
        case TokenKind.SYMBOL:
            car = Object(ObjectKind.SYMBOL, token.value)
            cdr = parse(tokens)
            return Object(ObjectKind.CONS, Cons(car, cdr))
        case _:
            raise RuntimeError(f"Unexpected token: {token}")


def eval(expr: Object):

    if not expr:
        return Object(ObjectKind.NIL, None)

    match expr.kind:
        case ObjectKind.INTEGER:
            return expr
        case ObjectKind.SYMBOL:
            return expr
        case ObjectKind.NIL:
            return expr
        case ObjectKind.OPERATOR:
            return expr
        case ObjectKind.CONS:
            car = expr.value.car
            cdr = expr.value.cdr

            # ここで関数適用を処理
            func = eval(car)
            if func is None:
                return Object(ObjectKind.NIL, None)

            # ここで引数を評価
            arg = eval(cdr)
            if arg is None:
                return Object(ObjectKind.NIL, None)

            if func.kind == ObjectKind.OPERATOR:
                match func.value.kind:
                    case OperatorKind.ADD:


def run(code):
    tokens = tokenize(code)
    print("tokens:", [str(token) for token in tokens])
    s_expr = parse(tokens)
    print("s_expr:", [str(d) for d in s_expr])
    result = eval(s_expr)
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
