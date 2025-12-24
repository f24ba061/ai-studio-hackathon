#!/usr/bin/env python3
import sqlite3
import os

# データベースパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
DB_NAME = os.path.join(project_root, 'data', 'tourism_review.db')

def add_test_user():
    """testユーザーをユーザーマスターに追加"""

    # データベースに接続
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # testユーザーのデータ
    test_user = ('test123', 'テストユーザー')  # (パスワード, 名前)

    try:
        # ユーザーを挿入
        cursor.execute(
            'INSERT INTO users (password, name) VALUES (?, ?)',
            test_user
        )
        conn.commit()

        # 登録したユーザーのIDを取得
        user_id = cursor.lastrowid
        print(f"✅ testユーザーを登録しました！")
        print(f"   ユーザーID: {user_id}")
        print(f"   パスワード: {test_user[0]}")
        print(f"   名前: {test_user[1]}")

        # 全ユーザーを確認
        print("\n=== 登録済みユーザー一覧 ===")
        cursor.execute('SELECT user_id, name FROM users')
        for row in cursor.fetchall():
            print(f"  ID: {row[0]:3d} | 名前: {row[1]}")

    except sqlite3.IntegrityError as e:
        print(f"❌ エラー: ユーザーの登録に失敗しました。{e}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_test_user()