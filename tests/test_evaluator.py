import unittest

from lispy.evaluator import Environment, create_global_env, eval_lisp


class TestEvaluator(unittest.TestCase):

    def test_eval_number(self):
        """数値リテラルの評価"""
        result = eval_lisp(42)
        self.assertEqual(result, 42)

    def test_eval_string_symbol(self):
        """シンボルの評価（変数参照）"""
        env = Environment()
        env.define('x', 10)
        result = eval_lisp('x', env)
        self.assertEqual(result, 10)

    def test_eval_undefined_symbol(self):
        """未定義シンボルのエラー"""
        with self.assertRaises(NameError):
            eval_lisp('undefined')

    def test_eval_addition(self):
        """加算の評価"""
        result = eval_lisp(['+', 1, 2])
        self.assertEqual(result, 3)

    def test_eval_addition_multiple(self):
        """複数値の加算"""
        result = eval_lisp(['+', 1, 2, 3, 4])
        self.assertEqual(result, 10)

    def test_eval_subtraction(self):
        """減算の評価"""
        result = eval_lisp(['-', 5, 3])
        self.assertEqual(result, 2)

    def test_eval_negation(self):
        """単項マイナス"""
        result = eval_lisp(['-', 5])
        self.assertEqual(result, -5)

    def test_eval_multiplication(self):
        """乗算の評価"""
        result = eval_lisp(['*', 3, 4])
        self.assertEqual(result, 12)

    def test_eval_multiplication_multiple(self):
        """複数値の乗算"""
        result = eval_lisp(['*', 2, 3, 4])
        self.assertEqual(result, 24)

    def test_eval_division(self):
        """除算の評価"""
        result = eval_lisp(['/', 10, 2])
        self.assertEqual(result, 5.0)

    def test_eval_nested_expression(self):
        """入れ子式の評価"""
        result = eval_lisp(['+', 1, ['*', 2, 3]])
        self.assertEqual(result, 7)

    def test_eval_complex_expression(self):
        """複雑な式の評価"""
        result = eval_lisp(['+', ['*', 2, 3], ['-', 10, 5]])
        self.assertEqual(result, 11)

    def test_eval_empty_list(self):
        """空リストの評価"""
        result = eval_lisp([])
        self.assertEqual(result, [])

    def test_eval_with_custom_env(self):
        """カスタム環境での評価"""
        env = create_global_env()  # グローバル環境をベースに
        env.define('x', 5)
        env.define('y', 10)
        result = eval_lisp(['+', 'x', 'y'], env)
        self.assertEqual(result, 15)

    def test_environment_parent_lookup(self):
        """親環境からの変数検索"""
        parent_env = Environment()
        parent_env.define('x', 42)

        child_env = Environment(parent_env)
        child_env.define('y', 10)

        result_x = eval_lisp('x', child_env)
        result_y = eval_lisp('y', child_env)

        self.assertEqual(result_x, 42)
        self.assertEqual(result_y, 10)

    def test_global_environment(self):
        """グローバル環境の確認"""
        env = create_global_env()

        # 基本演算子が定義されていることを確認
        self.assertTrue(callable(env.lookup('+')))
        self.assertTrue(callable(env.lookup('-')))
        self.assertTrue(callable(env.lookup('*')))
        self.assertTrue(callable(env.lookup('/')))

    def test_eval_non_callable_error(self):
        """呼び出し不可能なオブジェクトのエラー"""
        env = Environment()
        env.define('not_func', 42)

        with self.assertRaises(TypeError):
            eval_lisp(['not_func', 1, 2], env)


if __name__ == '__main__':
    unittest.main()
