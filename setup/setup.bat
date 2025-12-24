@echo off
chcp 65001 > nul

echo ===================================
echo 🏔️  群馬県観光地レビューアプリ
echo    Python版 セットアップ
echo ===================================
echo.

rem Python3の確認
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ エラー: Pythonがインストールされていません
    echo    https://www.python.org からインストールしてください
    pause
    exit /b 1
)

echo ✅ Pythonを確認しました
python --version
echo.

echo [1] 📦 必要なパッケージをインストール中...
pip install -r ../requirements.txt
if %errorlevel% neq 0 (
    echo ❌ エラー: パッケージのインストールに失敗しました
    echo    以下を個別に実行してみてください:
    echo    pip install flask flask-cors
    pause
    exit /b 1
)

echo.
echo [2] 🗄️  データベースを初期化中...
sqlite3 ../tourism_review.db < ../database/schema.sql
if %errorlevel% neq 0 (
    echo ❌ エラー: データベースの初期化に失敗しました
    pause
    exit /b 1
)

echo.
echo [3] 🏔️  群馬県観光地データを追加中...
python ../database/add_tourist_spots.py
if %errorlevel% neq 0 (
    echo ⚠️  警告: 観光地データの追加に失敗しました
)

echo.
echo [4] 👤 サンプルユーザーを追加中...
python ../database/add_sample_users.py
if %errorlevel% neq 0 (
    echo ⚠️  警告: サンプルユーザーの追加に失敗しました
)

echo.
echo [5] ⭐ サンプルレビューを追加中...
python ../database/add_sample_reviews.py
if %errorlevel% neq 0 (
    echo ⚠️  警告: サンプルレビューの追加に失敗しました
)

echo.
echo ===================================
echo 🎉 セットアップが完了しました！
echo ===================================
echo.
echo 🚀 サーバーを起動するには:
echo    python ../server.py
echo.
echo 🌐 ブラウザでアクセス:
echo    http://127.0.0.1:3001
echo    http://127.0.0.1:3001/spots.html
echo.
echo ⭐ テスト用ログイン情報:
echo    ユーザーID: 1
echo    パスワード: test123
echo.
echo 🛑 サーバーを停止するには: Ctrl + C
echo.
pause