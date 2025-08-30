import unittest

from lispy import run, tokenize

# LISPインタプリタの主要な関数（後で実装）
# parse(code) は文字列のコードをS式に変換する
# evaluate(s_expression) はS式を評価する
# run(code) はコード文字列全体を実行する

class TestLispInterpreter(unittest.TestCase):

    def test_add_expression(self):
        """
        テスト: 基本的な足し算のS式を評価できるか
        """
        # (1) 準備
        code = '(+ 1 2)'

        # (2) 実行
        result = run(code)

        # (3) 検証
        self.assertEqual(result, 3)

    def test_nested_add_expression(self):
        """
        テスト: 括弧の入れ子になった足し算を評価できるか
        """
        # (1) 準備
        code = '(+ 1 (+ 2 3))'

        # (2) 実行
        result = run(code)

        # (3) 検証
        self.assertEqual(result, 6)

    def test_single_number(self):
        """
        テスト: 単一の数値リテラルを評価できるか
        """
        # (1) 準備
        code = '42'

        # (2) 実行
        result = run(code)

        # (3) 検証
        self.assertEqual(result, 42)


class TestTokenizer(unittest.TestCase):
    """Tokenizerの動作をテストするクラス"""

    def test_simple_expression_tokenization(self):
        """
        テスト: 単純な式 '(+ 1 2)' が正しくトークン化されるか
        """
        # (1) 準備
        code = '(+ 1 2)'
        expected_tokens = [
            ('LPAREN', '('),
            ('OPERATOR', '+'),
            ('INTEGER', '1'),
            ('INTEGER', '2'),
            ('RPAREN', ')')
        ]

        # (2) 実行
        result = tokenize(code)

        # (3) 検証
        self.assertEqual(result, expected_tokens)

    def test_nested_expression_tokenization(self):
        """
        テスト: ネストした式 '(+ 1 (+ 2 3))' が正しくトークン化されるか
        """
        # (1) 準備
        code = '(+ 1 (+ 2 3))'
        expected_tokens = [
            ('LPAREN', '('),
            ('OPERATOR', '+'),
            ('INTEGER', '1'),
            ('LPAREN', '('),
            ('OPERATOR', '+'),
            ('INTEGER', '2'),
            ('INTEGER', '3'),
            ('RPAREN', ')'),
            ('RPAREN', ')')
        ]

        # (2) 実行
        result = tokenize(code)

        # (3) 検証
        self.assertEqual(result, expected_tokens)

    def test_number_tokenization(self):
        """
        テスト: 数値のトークン化が正しく動作するか
        """
        # (1) 準備
        code = '42'
        expected_tokens = [('INTEGER', '42')]

        # (2) 実行
        result = tokenize(code)

        # (3) 検証
        self.assertEqual(result, expected_tokens)

    def test_operator_tokenization(self):
        """
        テスト: 演算子のトークン化が正しく動作するか
        """
        # (1) 準備
        test_cases = [
            ('+', [('OPERATOR', '+')]),
            ('-', [('OPERATOR', '-')]),
            ('*', [('OPERATOR', '*')]),
            ('/', [('OPERATOR', '/')]),
        ]

        for code, expected_tokens in test_cases:
            with self.subTest(code=code):
                # (2) 実行
                result = tokenize(code)

                # (3) 検証
                self.assertEqual(result, expected_tokens)

    def test_symbol_tokenization(self):
        """
        テスト: シンボルのトークン化が正しく動作するか
        """
        # (1) 準備
        test_cases = [
            ('define', [('SYMBOL', 'define')]),
            ('my_var', [('SYMBOL', 'my_var')]),
            ('foo123', [('SYMBOL', 'foo123')]),
        ]

        for code, expected_tokens in test_cases:
            with self.subTest(code=code):
                # (2) 実行
                result = tokenize(code)

                # (3) 検証
                self.assertEqual(result, expected_tokens)

    def test_whitespace_handling(self):
        """
        テスト: 空白文字が適切に処理されるか（無視されるか）
        """
        # (1) 準備
        code = '  ( +   1    2  )  '
        expected_tokens = [
            ('LPAREN', '('),
            ('OPERATOR', '+'),
            ('INTEGER', '1'),
            ('INTEGER', '2'),
            ('RPAREN', ')')
        ]

        # (2) 実行
        result = tokenize(code)

        # (3) 検証
        self.assertEqual(result, expected_tokens)

    def test_complex_expression_tokenization(self):
        """
        テスト: より複雑な式のトークン化
        """
        # (1) 準備
        code = '(define square (lambda (x) (* x x)))'
        expected_tokens = [
            ('LPAREN', '('),
            ('SYMBOL', 'define'),
            ('SYMBOL', 'square'),
            ('LPAREN', '('),
            ('SYMBOL', 'lambda'),
            ('LPAREN', '('),
            ('SYMBOL', 'x'),
            ('RPAREN', ')'),
            ('LPAREN', '('),
            ('OPERATOR', '*'),
            ('SYMBOL', 'x'),
            ('SYMBOL', 'x'),
            ('RPAREN', ')'),
            ('RPAREN', ')'),
            ('RPAREN', ')')
        ]

        # (2) 実行
        result = tokenize(code)

        # (3) 検証
        self.assertEqual(result, expected_tokens)

    def test_empty_string_tokenization(self):
        """
        テスト: 空文字列のトークン化
        """
        # (1) 準備
        code = ''
        expected_tokens = []

        # (2) 実行
        result = tokenize(code)

        # (3) 検証
        self.assertEqual(result, expected_tokens)


def main():
    """テストを実行するメイン関数"""
    print("🧪 Running lispy tests...")
    unittest.main(verbosity=2, exit=False)


if __name__ == '__main__':
    main()