"""
LISP interpreter tokenizer module.

This module provides tokenization functionality for the LISP interpreter,
including token types and the main tokenize function.
"""

import re
from dataclasses import dataclass
from enum import Enum


class TokenKind(Enum):
    """Token types for the LISP tokenizer."""
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    INTEGER = "INTEGER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    SYMBOL = "SYMBOL"


@dataclass
class Token:
    """Represents a single token in the LISP source code."""
    kind: TokenKind
    value: str

    def __str__(self):
        return f"Token('{self.kind.value}', '{self.value}')"


def tokenize(code: str) -> list[Token]:
    """
    Tokenize LISP source code into tokens.

    Args:
        code: The LISP source code string to tokenize

    Returns:
        A list of Token objects representing the tokenized code

    Raises:
        RuntimeError: If an unexpected character is encountered
    """
    token_spec = {
        "LPAREN":     r"\(",
        "RPAREN":     r"\)",
        "INTEGER":    r"[0-9]+",
        "OPERATOR":   r"[+\-*/%=<>]|<=|>=",
        "STRING":     r'"(\\.|[^"\\])*"',
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
            case "STRING":
                tokens.append(Token(TokenKind.STRING, value))
            case "SYMBOL":
                tokens.append(Token(TokenKind.SYMBOL, value))
            case "WHITESPACE" | "NEWLINE":
                continue
            case "MISMATCH":
                raise RuntimeError(f"Unexpected character: {value}")
            case _:
                raise RuntimeError(f"Unknown token kind: {kind}")

    return tokens
