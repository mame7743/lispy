import unittest

from lispy import run

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


def main():
    """テストを実行するメイン関数"""
    print("🧪 Running lispy tests...")
    unittest.main(verbosity=2, exit=False)


if __name__ == '__main__':
    main()