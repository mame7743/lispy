import re
from dataclasses import dataclass
from encodings.punycode import T
from enum import Enum
from tkinter import NO, W


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
            return None
        case TokenKind.INTEGER:
            return int(token.value), parse(tokens)
        case TokenKind.SYMBOL:
            return token.value, parse(tokens)
        case _:
            raise RuntimeError(f"Unexpected token: {token}")


def eval(expr):

    if expr is None:
        return None

    car = expr['car']
    cdr = expr['cdr']

    if type(car) is dict:
        expr = eval(cdr)
        print("car:", car)
        if expr is None:
            return None
        # elif car['kind'] == "OPERATOR":
        #     if car['value'] == '+':
        #         return add_expr(cdr)
        #     if car['value'] == '-':
        #         return eval(cdr) - eval(cdr[1])
        #     if car['value'] == '*':
        #         return eval(cdr) * eval(cdr[1])
        #     if car['value'] == '/':
        #         return eval(cdr) / eval(cdr[1])
        else:
            return None
        
    else:
        
        if car['kind'] == "SYMBOL":
            return car['value']
        if car['kind'] == "FLOAT":
            return car['value']
        if car['kind'] == "INTEGER":
            return car['value']
    return None

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
