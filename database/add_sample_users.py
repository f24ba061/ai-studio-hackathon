#!/usr/bin/env python3
import sqlite3
import os
import sys

def get_db_path():
    """データベースファイルのパスを取得"""
    # 環境変数DB_PATHが設定されていればそれを使用（Docker用）
    db_path = os.environ.get('DB_PATH')
    if db_path:
        return db_path
    # 環境変数がなければデフォルトのパス（プロジェクトルート）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, 'data', 'tourism_review.db')

def add_sample_users():
    """サンプルユーザーをユーザーマスターに追加（testユーザーがID:1）"""

    # データベースに接続
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ユーザーデータ（testユーザーを最初に配置）
    sample_users = [
        (1, 'test123', 'テストユーザー'),       # ID:1 テストユーザー
        (2, 'password123', '山田太郎'),          # ID:2 サンプルユーザー1
        (3, 'password456', '佐藤花子'),          # ID:3 サンプルユーザー2
        (4, 'password789', '鈴木一郎')           # ID:4 サンプルユーザー3
    ]

    try:
        # 既存のユーザーを削除
        cursor.execute('DELETE FROM users')

        # ユーザーを挿入（user_idを明示的に指定）
        cursor.executemany(
            'INSERT INTO users (user_id, password, name) VALUES (?, ?, ?)',
            sample_users
        )

        # 自動増分カウンターを更新
        cursor.execute('UPDATE sqlite_sequence SET seq = 4 WHERE name = "users"')

        conn.commit()

        print(f"✅ {len(sample_users)}件のユーザーデータを追加しました！")
        print()

        # 登録済みユーザーを確認
        print("=== 登録済みユーザー一覧 ===")
        cursor.execute('SELECT user_id, password, name FROM users ORDER BY user_id')
        for row in cursor.fetchall():
            print(f"  ID: {row[0]:2d} | パスワード: {row[1]:12s} | 名前: {row[2]}")

        print()
        print("🔑 学生用ログイン情報:")
        print("   ユーザーID: 1")
        print("   パスワード: test123")

    except sqlite3.IntegrityError as e:
        print(f"❌ エラー: データの重複があります。{e}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_sample_users()