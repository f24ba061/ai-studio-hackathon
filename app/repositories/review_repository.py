from repositories.database import get_db, close_db

class ReviewRepository:
    """レビューテーブルへのデータアクセス"""

    def find_by_spot_id(self, spot_id):
        """観光地IDでレビューを取得（ユーザー名もJOINで取得）"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    r.review_id,
                    r.user_id,
                    r.spot_id,
                    r.review_content,
                    r.rating,
                    r.photo_filename,
                    r.created_at,
                    u.name AS user_name
                FROM reviews r
                LEFT JOIN users u
                    ON r.user_id = u.user_id
                WHERE r.spot_id = ?
                ORDER BY r.created_at DESC
            ''', (spot_id,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"レビュー取得エラー: {e}")
            return []
        finally:
            close_db(conn)

    def create(self, review_data):
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
            return cursor.lastrowid
        except Exception as e:
            print(f"レビュー作成エラー: {e}")
            return None
        finally:
            close_db(conn)

    def update_photo_filename(self, review_id, photo_filename):
        conn = get_db()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE reviews SET photo_filename = ? WHERE review_id = ?',
                (photo_filename, review_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"写真更新エラー: {e}")
            return False
        finally:
            close_db(conn)

    def find_by_id(self, review_id):
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM reviews WHERE review_id = ?', (review_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            close_db(conn)

    def delete(self, review_id):
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
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM reviews WHERE user_id = ? AND spot_id = ?',
                (user_id, spot_id)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            close_db(conn)