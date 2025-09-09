import unittest

from lispy.parser import ParseError, parse
from lispy.tokenizer import Token, TokenKind, tokenize


class TestParser(unittest.TestCase):

    def test_parse_empty_input(self):
        """
        テスト: 空の入力のパース
        """
        tokens = []
        result = parse(tokens)
        self.assertEqual(result, [])

    def test_parse_single_integer(self):
        """
        テスト: 単一の整数のパース
        """
        tokens = [Token(TokenKind.INTEGER, "42")]
        result = parse(tokens)
        self.assertEqual(result, [42])

    def test_parse_single_symbol(self):
        """
        テスト: 単一のシンボルのパース
        """
        tokens = [Token(TokenKind.SYMBOL, "x")]
        result = parse(tokens)
        self.assertEqual(result, ["x"])

    def test_parse_single_operator(self):
        """
        テスト: 単一の演算子のパース
        """
        tokens = [Token(TokenKind.OPERATOR, "+")]
        result = parse(tokens)
        self.assertEqual(result, ["+"])

    def test_parse_simple_expression(self):
        """
        テスト: 単純な算術式のパース
        """
        code = "(+ 1 2)"
        tokens = tokenize(code)
        result = parse(tokens)
        expected = [["+", 1, 2]]
        self.assertEqual(result, expected)

    def test_parse_nested_expression(self):
        """
        テスト: 入れ子の式のパース
        """
        code = "(+ 1 (* 2 3))"
        tokens = tokenize(code)
        result = parse(tokens)
        expected = [["+", 1, ["*", 2, 3]]]
        self.assertEqual(result, expected)

    def test_parse_multiple_expressions(self):
        """
        テスト: 複数の式のパース
        """
        code = "42 (+ 1 2) x"
        tokens = tokenize(code)
        result = parse(tokens)
        expected = [42, ["+", 1, 2], "x"]
        self.assertEqual(result, expected)

    def test_parse_complex_nested_expression(self):
        """
        テスト: 複雑な入れ子の式のパース
        """
        code = "(+ (* 2 3) (- 10 5))"
        tokens = tokenize(code)
        result = parse(tokens)
        expected = [["+", ["*", 2, 3], ["-", 10, 5]]]
        self.assertEqual(result, expected)

    def test_parse_symbol_with_numbers(self):
        """
        テスト: 数字を含むシンボルのパース
        """
        code = "(define x1 42)"
        tokens = tokenize(code)
        result = parse(tokens)
        expected = [["define", "x1", 42]]
        self.assertEqual(result, expected)

    def test_parse_missing_closing_paren(self):
        """
        テスト: 閉じ括弧が不足している場合のエラー
        """
        tokens = [
            Token(TokenKind.LPAREN, "("),
            Token(TokenKind.OPERATOR, "+"),
            Token(TokenKind.INTEGER, "1"),
            Token(TokenKind.INTEGER, "2")
        ]
        with self.assertRaises(ParseError):
            parse(tokens)

    def test_parse_unexpected_closing_paren(self):
        """
        テスト: 予期しない閉じ括弧のエラー
        """
        tokens = [Token(TokenKind.RPAREN, ")")]
        with self.assertRaises(ParseError):
            parse(tokens)

    def test_parse_empty_list(self):
        """
        テスト: 空のリストのパース
        """
        code = "()"
        tokens = tokenize(code)
        result = parse(tokens)
        expected = [[]]
        self.assertEqual(result, expected)

    def test_parse_deeply_nested_expression(self):
        """
        テスト: 深く入れ子になった式のパース
        """
        code = "(+ 1 (+ 2 (+ 3 4)))"
        tokens = tokenize(code)
        result = parse(tokens)
        expected = [["+", 1, ["+", 2, ["+", 3, 4]]]]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
