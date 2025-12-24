#!/bin/bash
set -e

echo "=========================================="
echo "🚀 群馬県観光地レビューアプリ起動中..."
echo "=========================================="

# データベースディレクトリを作成
mkdir -p /app/data

# データベースファイルのパスを設定
export DB_PATH="/app/data/tourism_review.db"

# データベースが存在しない場合は初期化
if [ ! -f "$DB_PATH" ]; then
    echo "📦 データベースを初期化しています..."

    # データベースを初期化
    cd /app
    python3 database/init_db.py

    # 観光地データを追加
    echo "🗾 観光地データを追加しています..."
    python3 database/add_tourist_spots.py

    # サンプルユーザーを追加
    echo "👤 サンプルユーザーを追加しています..."
    python3 database/add_sample_users.py

    # サンプルレビューを追加
    echo "⭐ サンプルレビューを追加しています..."
    python3 database/add_sample_reviews.py

    # サンプルイベントを追加
    echo "🎭 サンプルイベントを追加しています..."
    python3 database/add_sample_events.py

    # 画像付きレビューを追加
    echo "📸 画像付きレビューを追加しています..."
    python3 database/add_photo_review.py

    echo "✅ データベース初期化完了"
else
    echo "✅ 既存のデータベースを使用します"
fi

echo ""
echo "=========================================="
echo "📍 サーバーを起動します"
echo "   ブラウザで以下にアクセス:"
echo "   🌐 http://localhost:3001"
echo "   📋 観光地一覧: http://localhost:3001/spots.html"
echo ""
echo "⭐ テスト用ログイン情報:"
echo "   ユーザーID: 1"
echo "   パスワード: test123"
echo "=========================================="

# Flaskアプリケーションを起動
cd /app/app
python3 app.py
