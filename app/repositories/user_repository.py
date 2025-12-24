"""
ユーザーデータへのアクセスを担当
"""
from repositories.database import get_db, close_db

class UserRepository:
    """ユーザーテーブルへのデータアクセス"""

    def find_by_id(self, user_id):
        """IDでユーザーを取得"""
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"ユーザー取得エラー: {e}")
            return None
        finally:
            close_db(conn)

    def find_by_credentials(self, user_id, password):
        """認証情報でユーザーを取得"""
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE user_id = ? AND password = ?',
                (user_id, password)
            )
            user = cursor.fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"ユーザー認証エラー: {e}")
            return None
        finally:
            close_db(conn)

    def create(self, user_data):
        """ユーザーを作成"""
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (password, name) VALUES (?, ?)',
                (user_data['password'], user_data['name'])
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except Exception as e:
            print(f"ユーザー作成エラー: {e}")
            return None
        finally:
            close_db(conn)
