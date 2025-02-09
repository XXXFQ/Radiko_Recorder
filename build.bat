@echo off
echo Build start...

:: PowerShellコマンドでUPXのパスを取得
for /f "usebackq tokens=*" %%i in (`powershell -Command "(Get-Command upx.exe).Path | Split-Path"`) do set UPX_DIR=%%i

:: UPXのパスが見つからない場合エラーを表示
if "%UPX_DIR%"=="" (
    echo Error: UPX not found in PATH.
    echo Please ensure UPX is installed and its directory is in the PATH environment variable.
    pause
    exit /b 1
)

:: UPXのパスを確認
echo UPX Directory: %UPX_DIR%

:: 仮想環境でPyInstallerを実行
uv run pyinstaller --onefile --name radiko-recorder -c --hidden-import=radiko_recorder --upx-dir "%UPX_DIR%" -p ./radiko_recorder radiko_recorder/__main__.py

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo Build complete!
pause