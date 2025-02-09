#!/bin/bash

echo "Build start..."

# UPXのパスを取得
UPX_PATH=$(command -v upx)

# UPXのパスが見つからない場合エラーを表示
if [ -z "$UPX_PATH" ]; then
    echo "Error: UPX not found in PATH."
    echo "Please ensure UPX is installed and its directory is in the PATH environment variable."
    exit 1
fi

# UPXのディレクトリを取得
UPX_DIR=$(dirname "$UPX_PATH")
echo "UPX Directory: $UPX_DIR"

# 仮想環境でPyInstallerを実行
uv run pyinstaller --onefile --name radiko-recorder -c --hidden-import=radiko_recorder --upx-dir "$UPX_DIR" -p ./radiko_recorder radiko_recorder/__main__.py

# ビルドが成功したかを確認
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

echo "Build complete!"