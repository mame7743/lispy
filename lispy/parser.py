"""
LISP interpreter parser module.

This module provides parsing functionality to convert tokens into
abstract syntax trees (S-expressions).
"""

from typing import Any

from .tokenizer import Token, TokenKind


class ParseError(Exception):
    """Raised when parsing fails."""


def parse(tokens: list[Token]) -> list[Any]:
    """
    Parse tokens into S-expressions.

    Args:
        tokens: List of tokens to parse

    Returns:
        List of parsed S-expressions

    Raises:
        ParseError: If parsing fails
    """
    if not tokens:
        return []

    expressions = []
    i = 0

    while i < len(tokens):
        expr, i = parse_expression(tokens, i)
        expressions.append(expr)

    return expressions


def parse_expression(tokens: list[Token], start: int) -> tuple[Any, int]:
    """
    Parse a single expression starting at the given index.

    Args:
        tokens: List of tokens
        start: Starting index

    Returns:
        Tuple of (parsed_expression, next_index)

    Raises:
        ParseError: If parsing fails
    """
    if start >= len(tokens):
        raise ParseError("Unexpected end of input")

    token = tokens[start]

    if token.kind == TokenKind.LPAREN:
        # Parse list expression
        return parse_list(tokens, start + 1)
    elif token.kind == TokenKind.INTEGER:
        # Parse integer
        return int(token.value), start + 1
    elif token.kind == TokenKind.OPERATOR:
        # Parse operator as symbol
        return token.value, start + 1
    elif token.kind == TokenKind.SYMBOL:
        # Parse symbol
        return token.value, start + 1
    else:
        raise ParseError(f"Unexpected token: {token}")


def parse_list(tokens: list[Token], start: int) -> tuple[list[Any], int]:
    """
    Parse a list expression starting after the opening parenthesis.

    Args:
        tokens: List of tokens
        start: Starting index (after LPAREN)

    Returns:
        Tuple of (parsed_list, next_index)

    Raises:
        ParseError: If parsing fails
    """
    elements = []
    i = start

    while i < len(tokens) and tokens[i].kind != TokenKind.RPAREN:
        expr, i = parse_expression(tokens, i)
        elements.append(expr)

    if i >= len(tokens):
        raise ParseError("Missing closing parenthesis")

    # Skip the closing parenthesis
    return elements, i + 1
