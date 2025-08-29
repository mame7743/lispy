#!/bin/bash

# スクリプトの実行に失敗した場合、直ちに終了する
set -e

echo "どのファイルをコミットに含めますか？"
echo "番号をスペースで区切って複数入力してください（例: 1 3 5）。'a' で全て、'q' で終了。"

# 変更されたファイルのリストを配列に格納
declare -a files=($(git status --porcelain=v1 | awk '{print $2}'))

if [[ ${#files[@]} -eq 0 ]]; then
    echo "コミットする変更がありません。処理を終了します。"
    exit 1
fi

# 選択肢の表示
for i in "${!files[@]}"; do
    printf "[%s] %s\n" $((i+1)) "${files[$i]}"
done
printf "[a] すべてのファイルをコミット\n"
printf "[q] 終了\n"

# ユーザーからの入力を受け取る
read -p "> " selections

# 入力内容を解析
if [[ "$selections" == "a" ]]; then
    echo "すべての差分ファイルをステージングします。"
    git add .
elif [[ "$selections" == "q" ]]; then
    echo "処理を中止します。"
    exit 0
else
    # 選択された番号に基づいてファイルをステージング
    for selection in $selections; do
        index=$((selection-1))
        if [[ $index -ge 0 && $index -lt ${#files[@]} ]]; then
            file_to_add="${files[$index]}"
            echo "'$file_to_add' をステージングしました。"
            git add "$file_to_add"
        else
            echo "無効な番号 '$selection' です。処理を中止します。"
            exit 1
        fi
    done
fi

echo "コミットメッセージを生成します。"
# Commitizenの対話式インターフェースを呼び出す
uv run cz commit