#!/bin/bash

echo "==================================="
echo "🏔️  群馬県観光地レビューアプリ"
echo "   Python版 セットアップ"
echo "==================================="
echo

# Python3の確認
if ! command -v python3 &> /dev/null; then
    echo "❌ エラー: Python3がインストールされていません"
    echo "   https://www.python.org からインストールしてください"
    exit 1
fi

echo "✅ Python3を確認しました"
python3 --version
echo

echo "[1] 📦 必要なパッケージをインストール中..."
pip3 install -r ../requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ エラー: パッケージのインストールに失敗しました"
    echo "   以下を個別に実行してみてください:"
    echo "   pip3 install flask flask-cors"
    exit 1
fi

echo
echo "[2] 🗄️  データベースを初期化中..."
sqlite3 ../tourism_review.db < ../database/schema.sql
if [ $? -ne 0 ]; then
    echo "❌ エラー: データベースの初期化に失敗しました"
    exit 1
fi

echo
echo "[3] 🏔️  群馬県観光地データを追加中..."
python3 ../database/add_tourist_spots.py
if [ $? -ne 0 ]; then
    echo "⚠️  警告: 観光地データの追加に失敗しました"
fi

echo
echo "[4] 👤 サンプルユーザーを追加中..."
python3 ../database/add_sample_users.py
if [ $? -ne 0 ]; then
    echo "⚠️  警告: サンプルユーザーの追加に失敗しました"
fi

echo
echo "[5] ⭐ サンプルレビューを追加中..."
python3 ../database/add_sample_reviews.py
if [ $? -ne 0 ]; then
    echo "⚠️  警告: サンプルレビューの追加に失敗しました"
fi

echo
echo "==================================="
echo "🎉 セットアップが完了しました！"
echo "==================================="
echo
echo "🚀 サーバーを起動するには:"
echo "   python3 ../server.py"
echo
echo "🌐 ブラウザでアクセス:"
echo "   http://127.0.0.1:3001"
echo "   http://127.0.0.1:3001/spots.html"
echo
echo "⭐ テスト用ログイン情報:"
echo "   ユーザーID: 1"
echo "   パスワード: test123"
echo
echo "🛑 サーバーを停止するには: Ctrl + C"
echo