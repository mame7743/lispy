# LISPY

A simple LISP interpreter implemented in Python.

LISPのS式をPythonで解釈するインタプリタを作成するプロジェクトです。

## Installation

```bash
pip install -e .
```

## Usage

### Command Line
```bash
lispy
```

### Python Module
```python
from lispy import repl
repl()
```

## Development

### Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing
```bash
# Run tests
python -m pytest tests/

# Run with unittest
python -m unittest discover tests/
```

### Project Structure
```
lispy/
├── lispy/              # Main package
│   ├── __init__.py
│   ├── tokenizer.py    # Tokenization
│   ├── lisp_parser.py  # Parsing
│   ├── evaluator.py    # Evaluation
│   └── lispy.py        # Main logic
├── tests/              # Test suite
│   ├── __init__.py
│   └── test_tokenizer.py
├── main.py             # Development entry point
└── pyproject.toml      # Project configuration
```

## 実装

このプロジェクトは、以下のステップで進行します。

### ステップ１

このステップでのゴールは、`(+ 1 2)`というLISPのS式をPythonのリストとして解釈し、
最終的に3という結果を返すことです。

入力
- 文字列 `'(+ 1 2)'`

期待される出力
- 整数 `3`

## Features

- [x] Tokenization
- [ ] Parsing
- [ ] Evaluation
- [ ] Built-in functions
- [ ] Variable binding
- [ ] Function definition