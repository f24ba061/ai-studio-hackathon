#!/usr/bin/env python3
"""
データベース初期化スクリプト
tourism_review.dbを作成し、必要なテーブルとトリガーを作成します。
"""

import sqlite3
import os
import sys

def get_db_path():
    """データベースファイルのパスを取得"""
    # 環境変数DB_PATHが設定されていればそれを使用（Docker用）
    db_path = os.environ.get('DB_PATH')
    if db_path:
        return db_path

    # 環境変数がなければデフォルトのパス（data/ディレクトリ）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, 'data', 'tourism_review.db')

def init_database():
    """データベースを初期化"""
    db_path = get_db_path()

    print(f"📦 データベースを初期化します: {db_path}")

    # データベースディレクトリが存在しない場合は作成
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # データベースファイルが既に存在する場合は削除
    if os.path.exists(db_path):
        print(f"⚠️  既存のデータベースを削除します: {db_path}")
        os.remove(db_path)

    # データベース接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ===== テーブル作成 =====

    # ユーザーマスターテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 観光地マスターテーブル（avg_rating と review_count を追加）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tourist_spots (
            spot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_name TEXT NOT NULL,
            address TEXT,
            access TEXT,
            business_hours TEXT,
            fee TEXT,
            map_url TEXT,
            description TEXT,
            avg_rating REAL DEFAULT 0.0,
            review_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # レビューデータテーブル（photo_filename と UNIQUE制約を追加）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            spot_id INTEGER NOT NULL,
            review_content TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            photo_filename TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (spot_id) REFERENCES tourist_spots(spot_id) ON DELETE CASCADE,
            UNIQUE(user_id, spot_id)
        )
    ''')

    # イベントマスターテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            location TEXT,
            area TEXT,
            category TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ===== インデックス作成 =====

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reviews_user ON reviews(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reviews_spot ON reviews(spot_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_area ON events(area)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_date ON events(event_date)')

    # ===== トリガー作成（評価の自動更新） =====

    # トリガー1: レビュー追加時に平均評価を更新
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_rating_on_insert
        AFTER INSERT ON reviews
        FOR EACH ROW
        BEGIN
            UPDATE tourist_spots
            SET avg_rating = (
                    SELECT AVG(rating)
                    FROM reviews
                    WHERE spot_id = NEW.spot_id
                ),
                review_count = (
                    SELECT COUNT(*)
                    FROM reviews
                    WHERE spot_id = NEW.spot_id
                )
            WHERE spot_id = NEW.spot_id;
        END
    ''')

    # トリガー2: レビュー削除時に平均評価を更新
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_rating_on_delete
        AFTER DELETE ON reviews
        FOR EACH ROW
        BEGIN
            UPDATE tourist_spots
            SET avg_rating = COALESCE(
                    (SELECT AVG(rating)
                     FROM reviews
                     WHERE spot_id = OLD.spot_id),
                    0.0
                ),
                review_count = (
                    SELECT COUNT(*)
                    FROM reviews
                    WHERE spot_id = OLD.spot_id
                )
            WHERE spot_id = OLD.spot_id;
        END
    ''')

    # トリガー3: レビュー更新時に平均評価を更新
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_rating_on_update
        AFTER UPDATE OF rating ON reviews
        FOR EACH ROW
        BEGIN
            UPDATE tourist_spots
            SET avg_rating = (
                    SELECT AVG(rating)
                    FROM reviews
                    WHERE spot_id = NEW.spot_id
                ),
                review_count = (
                    SELECT COUNT(*)
                    FROM reviews
                    WHERE spot_id = NEW.spot_id
                )
            WHERE spot_id = NEW.spot_id;
        END
    ''')

    conn.commit()
    conn.close()

    print("✅ データベース初期化が完了しました")
    print(f"   - データベースパス: {db_path}")
    print("   - テーブル: users, tourist_spots, reviews, events")
    print("   - トリガー: 評価自動更新（insert/delete/update）")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)
