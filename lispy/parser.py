"""
LISPインタープリターのパーサーモジュール

トークンをS式に変換する
"""

from typing import Any

from .tokenizer import Token, TokenKind


class ParseError(Exception):
    """パースエラー"""


def parse(tokens: list[Token]) -> list[Any]:
    """トークンリストをS式リストに変換"""
    if not tokens:
        return []

    expressions = []
    i = 0

    while i < len(tokens):
        expr, i = parse_expression(tokens, i)
        expressions.append(expr)

    return expressions


def parse_expression(tokens: list[Token], start: int) -> tuple[Any, int]:
    """単一の式をパースする"""
    if start >= len(tokens):
        raise ParseError("Unexpected end of input")

    token = tokens[start]

    if token.kind == TokenKind.LPAREN:
        return parse_list(tokens, start + 1)
    elif token.kind == TokenKind.INTEGER:
        return int(token.value), start + 1
    elif token.kind == TokenKind.STRING:
        # 文字列リテラルをタプルで包んで区別
        return ('STRING_LITERAL', token.value[1:-1]), start + 1
    elif token.kind == TokenKind.OPERATOR:
        return token.value, start + 1
    elif token.kind == TokenKind.SYMBOL:
        return token.value, start + 1
    else:
        raise ParseError(f"Unexpected token: {token}")


def parse_list(tokens: list[Token], start: int) -> tuple[list[Any], int]:
    """リスト式をパースする（開き括弧の後から）"""
    elements = []
    i = start

    while i < len(tokens) and tokens[i].kind != TokenKind.RPAREN:
        expr, i = parse_expression(tokens, i)
        elements.append(expr)

    if i >= len(tokens):
        raise ParseError("Missing closing parenthesis")

    return elements, i + 1
