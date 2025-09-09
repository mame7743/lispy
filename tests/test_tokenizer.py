import unittest

from lispy.tokenizer import Token, TokenKind, tokenize


class TestTokenizer(unittest.TestCase):

    def test_tokenize_simple_expression(self):
        """
        テスト: 基本的な算術式のトークン化
        """
        code = "(+ 1 2)"
        tokens = tokenize(code)

        expected = [
            Token(TokenKind.LPAREN, "("),
            Token(TokenKind.OPERATOR, "+"),
            Token(TokenKind.INTEGER, "1"),
            Token(TokenKind.INTEGER, "2"),
            Token(TokenKind.RPAREN, ")")
        ]

        self.assertEqual(len(tokens), len(expected))
        for i, (actual, expected_token) in enumerate(zip(tokens, expected)):
            self.assertEqual(actual.kind, expected_token.kind, f"Token {i}: kind mismatch")
            self.assertEqual(actual.value, expected_token.value, f"Token {i}: value mismatch")

    def test_tokenize_nested_expression(self):
        """
        テスト: 入れ子の式のトークン化
        """
        code = "(+ 1 (* 2 3))"
        tokens = tokenize(code)

        expected = [
            Token(TokenKind.LPAREN, "("),
            Token(TokenKind.OPERATOR, "+"),
            Token(TokenKind.INTEGER, "1"),
            Token(TokenKind.LPAREN, "("),
            Token(TokenKind.OPERATOR, "*"),
            Token(TokenKind.INTEGER, "2"),
            Token(TokenKind.INTEGER, "3"),
            Token(TokenKind.RPAREN, ")"),
            Token(TokenKind.RPAREN, ")")
        ]

        self.assertEqual(len(tokens), len(expected))
        for i, (actual, expected_token) in enumerate(zip(tokens, expected)):
            self.assertEqual(actual.kind, expected_token.kind, f"Token {i}: kind mismatch")
            self.assertEqual(actual.value, expected_token.value, f"Token {i}: value mismatch")

    def test_tokenize_with_symbols(self):
        """
        テスト: シンボル（変数名）を含む式のトークン化
        """
        code = "(define x 42)"
        tokens = tokenize(code)

        expected = [
            Token(TokenKind.LPAREN, "("),
            Token(TokenKind.SYMBOL, "define"),
            Token(TokenKind.SYMBOL, "x"),
            Token(TokenKind.INTEGER, "42"),
            Token(TokenKind.RPAREN, ")")
        ]

        self.assertEqual(len(tokens), len(expected))
        for i, (actual, expected_token) in enumerate(zip(tokens, expected)):
            self.assertEqual(actual.kind, expected_token.kind, f"Token {i}: kind mismatch")
            self.assertEqual(actual.value, expected_token.value, f"Token {i}: value mismatch")

    def test_tokenize_single_number(self):
        """
        テスト: 単一の数値のトークン化
        """
        code = "42"
        tokens = tokenize(code)

        expected = [Token(TokenKind.INTEGER, "42")]

        self.assertEqual(len(tokens), len(expected))
        self.assertEqual(tokens[0].kind, expected[0].kind)
        self.assertEqual(tokens[0].value, expected[0].value)

    def test_tokenize_whitespace_handling(self):
        """
        テスト: 空白文字の処理
        """
        code = "  ( +   1    2  )  "
        tokens = tokenize(code)

        expected = [
            Token(TokenKind.LPAREN, "("),
            Token(TokenKind.OPERATOR, "+"),
            Token(TokenKind.INTEGER, "1"),
            Token(TokenKind.INTEGER, "2"),
            Token(TokenKind.RPAREN, ")")
        ]

        self.assertEqual(len(tokens), len(expected))
        for i, (actual, expected_token) in enumerate(zip(tokens, expected)):
            self.assertEqual(actual.kind, expected_token.kind, f"Token {i}: kind mismatch")
            self.assertEqual(actual.value, expected_token.value, f"Token {i}: value mismatch")

    def test_tokenize_all_operators(self):
        """
        テスト: 全ての算術演算子のトークン化
        """
        code = "(+ - * /)"
        tokens = tokenize(code)

        expected = [
            Token(TokenKind.LPAREN, "("),
            Token(TokenKind.OPERATOR, "+"),
            Token(TokenKind.OPERATOR, "-"),
            Token(TokenKind.OPERATOR, "*"),
            Token(TokenKind.OPERATOR, "/"),
            Token(TokenKind.RPAREN, ")")
        ]

        self.assertEqual(len(tokens), len(expected))
        for i, (actual, expected_token) in enumerate(zip(tokens, expected)):
            self.assertEqual(actual.kind, expected_token.kind, f"Token {i}: kind mismatch")
            self.assertEqual(actual.value, expected_token.value, f"Token {i}: value mismatch")

    def test_tokenize_multi_digit_numbers(self):
        """
        テスト: 複数桁の数値のトークン化
        """
        code = "(+ 123 456)"
        tokens = tokenize(code)

        expected = [
            Token(TokenKind.LPAREN, "("),
            Token(TokenKind.OPERATOR, "+"),
            Token(TokenKind.INTEGER, "123"),
            Token(TokenKind.INTEGER, "456"),
            Token(TokenKind.RPAREN, ")")
        ]

        self.assertEqual(len(tokens), len(expected))
        for i, (actual, expected_token) in enumerate(zip(tokens, expected)):
            self.assertEqual(actual.kind, expected_token.kind, f"Token {i}: kind mismatch")
            self.assertEqual(actual.value, expected_token.value, f"Token {i}: value mismatch")

    def test_tokenize_empty_string(self):
        """
        テスト: 空文字列のトークン化
        """
        code = ""
        tokens = tokenize(code)
        self.assertEqual(len(tokens), 0)

    def test_tokenize_only_whitespace(self):
        """
        テスト: 空白文字のみの文字列のトークン化
        """
        code = "   \n\t  "
        tokens = tokenize(code)
        self.assertEqual(len(tokens), 0)


if __name__ == '__main__':
    unittest.main()
