#!/bin/bash
set -e

# --- 1. Python環境のセットアップ ---
echo "⚙️ Python仮想環境をセットアップしています..."
if [ ! -d ".venv" ]; then
    uv venv
fi

source .venv/bin/activate

# 必要なパッケージが未インストールなら追加
if ! uv pip list | grep -q pre-commit; then
    uv add pre-commit --dev
fi
if ! uv pip list | grep -q commitizen; then
    uv add commitizen --dev
fi

echo "✅ Python環境のセットアップが完了しました。"

# --- 2. Git環境とコミット設定のセットアップ ---
echo "🛠️ Gitフックとコミット設定をセットアップしています..."

# pre-commitフックをインストール（既存のものを上書き）
uv run pre-commit install --hook-type pre-commit --overwrite
uv run pre-commit install --hook-type commit-msg --overwrite

echo "✅ Gitフックが設定されました。"

# --- 3. 初期コミットの作成 ---
FILES=".gitignore README.md" # gitignoreとREADMEは必ず含める
FILES="$FILES .pre-commit-config.yaml pyproject.toml .python-version"
FILES="$FILES interactive-commit.sh"
if [ -f "uv.lock" ]; then
    FILES="$FILES uv.lock"
fi
git add $FILES

if git log --oneline | grep -q "Initial commit with core files"; then
    echo "既にイニシャルコミットが存在します。処理を終了します。"
    exit 0
fi

if [ -z "$(git diff --cached)" ]; then
    echo "コミットするファイルがありません。処理を終了します。"
    exit 0
fi

git commit -m "🎉 feat: Initial commit with core files"
echo "イニシャルコミットが完了しました。"