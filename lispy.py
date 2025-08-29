def tokenize(code):
    # ここにLISPのトークナイズロジックを実装します
    return code.split()

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
