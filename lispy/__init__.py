"""
LISPY interpreter package.

This package provides a complete LISPY interpreter implementation including
tokenization, parsing, evaluation, and REPL functionality.
"""

from .evaluator import eval_lisp
from .parser import parse
from .tokenizer import Token, TokenKind, tokenize

__version__ = "0.1.0"

__all__ = [
    'Token',
    'TokenKind',
    'tokenize',
    'parse',
    'eval_lisp',
]


def main():
    """Main entry point for the CLI."""
    from .lispy import main as lispy_main
    lispy_main()
