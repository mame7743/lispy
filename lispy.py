import re


def tokenize(code):

    token_spec = {}

    token_spec["LPAREN"] = r"\(" # 左括弧
    token_spec["RPAREN"] = r"\)" # 右括弧
    token_spec["INTEGER"] = r"[0-9]+" # 数字
    token_spec["OPERATOR"] = r"[+\-*/]" # 演算子
    token_spec["SYMBOL"] = r"[a-zA-Z_][a-zA-Z0-9_]*" # シンボル
    token_spec["WHITESPACE"] = r"\s+" # 空白
    token_spec["NEWLINE"] = r"\n" # 改行
    token_spec["MISMATCH"] = r"." # 不明なトークン

    tok_regex = "|".join(f"(?P<{name}>{pattern})"
                         for name, pattern in token_spec.items())
    get_token = re.compile(tok_regex).finditer

    tokens = []
    for m in get_token(code):
        kind = m.lastgroup
        value = m.group()

        print(f"Token: {kind}, Value: {value}")

        if kind in ('WHITESPACE', 'NEWLINE'):
            continue

        if kind == 'MISMATCH':
            raise RuntimeError(f"Unexpected token: {value}")

        tokens.append((kind, value))

    print(tokens)

    return tokens


def parse(code):
    # ここにLISPのパースロジックを実装します
    tokens = tokenize(code)
    return tokens

def eval(expr):
    # ここにLISPの評価ロジックを実装します
    return expr

def run(code):
    s_expr = parse(code)
    result = eval(s_expr)
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
