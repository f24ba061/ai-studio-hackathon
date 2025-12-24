"""
レビューデータへのアクセスを担当
"""
from repositories.database import get_db, close_db

class ReviewRepository:
    """レビューテーブルへのデータアクセス"""

    def find_by_spot_id(self, spot_id):
        """観光地IDでレビューを取得"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            # N+1クエリ問題
            # JOINを使わずにレビューだけ取得している
            # ユーザー名は後でservice層でループして取得することになり、N+1問題が発生する
            # 本来は JOIN users ON r.user_id = u.user_id でユーザー名も一緒に取得すべき
            cursor.execute('''
                SELECT *
                FROM reviews
                WHERE spot_id = ?
                ORDER BY created_at DESC
            ''', (spot_id,))
            reviews = [dict(row) for row in cursor.fetchall()]
            return reviews
        except Exception as e:
            print(f"レビュー取得エラー: {e}")
            return []
        finally:
            close_db(conn)

    def create(self, review_data):
        """レビューを作成"""
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reviews (user_id, spot_id, review_content, rating)
                VALUES (?, ?, ?, ?)
            ''', (
                review_data['user_id'],
                review_data['spot_id'],
                review_data['review_content'],
                review_data['rating']
            ))
            conn.commit()
            review_id = cursor.lastrowid
            return review_id
        except Exception as e:
            print(f"レビュー作成エラー: {e}")
            return None
        finally:
            close_db(conn)

    def update_photo_filename(self, review_id, photo_filename):
        """レビューの写真ファイル名を更新"""
        conn = get_db()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE reviews
                SET photo_filename = ?
                WHERE review_id = ?
            ''', (photo_filename, review_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"写真ファイル名更新エラー: {e}")
            return False
        finally:
            close_db(conn)

    def find_by_id(self, review_id):
        """IDでレビューを取得"""
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM reviews WHERE review_id = ?', (review_id,))
            review = cursor.fetchone()
            return dict(review) if review else None
        except Exception as e:
            print(f"レビュー取得エラー: {e}")
            return None
        finally:
            close_db(conn)

    def delete(self, review_id):
        """レビューを削除"""
        conn = get_db()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM reviews WHERE review_id = ?', (review_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"レビュー削除エラー: {e}")
            return False
        finally:
            close_db(conn)

    def find_by_user_and_spot(self, user_id, spot_id):
        """特定ユーザーの特定観光地へのレビューを取得"""
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM reviews WHERE user_id = ? AND spot_id = ?',
                (user_id, spot_id)
            )
            review = cursor.fetchone()
            return dict(review) if review else None
        except Exception as e:
            print(f"レビュー取得エラー: {e}")
            return None
        finally:
            close_db(conn)
