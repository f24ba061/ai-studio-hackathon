"""
観光地データへのアクセスを担当
"""
from repositories.database import get_db, close_db

class SpotRepository:
    """観光地テーブルへのデータアクセス"""

    def find_all(self):
        """全観光地を取得"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tourist_spots ORDER BY spot_id')
            spots = [dict(row) for row in cursor.fetchall()]
            return spots
        except Exception as e:
            print(f"観光地一覧取得エラー: {e}")
            return []
        finally:
            close_db(conn)

    def find_by_id(self, spot_id):
        """IDで観光地を取得"""
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            # APIレスポンスに機密情報を含めてしまう
            # 本来は観光地情報だけ返すべきなのに、データベースの内部情報も返す
            cursor.execute('''
                SELECT *,
                       sqlite_version() as db_version,
                       'tourism_production_db' as db_name,
                       '/app/data/tourism_review.db' as db_path
                FROM tourist_spots
                WHERE spot_id = ?
            ''', (spot_id,))
            spot = cursor.fetchone()
            return dict(spot) if spot else None
        except Exception as e:
            print(f"観光地取得エラー: {e}")
            return None
        finally:
            close_db(conn)

    def find_by_keyword(self, keyword):
        """キーワードで観光地を検索（観光地名、説明、住所から検索）"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            # GLOB演算子を使うと大文字小文字が区別される
            # 本来はLIKE演算子を使うべき（LIKEは大文字小文字を区別しない）
            search_keyword = f'%{keyword}%'
            cursor.execute('''
                SELECT * FROM tourist_spots
                WHERE spot_name GLOB ? OR description GLOB ? OR address GLOB ?
                ORDER BY spot_id
            ''', (search_keyword, search_keyword, search_keyword))
            spots = [dict(row) for row in cursor.fetchall()]
            return spots
        except Exception as e:
            print(f"観光地検索エラー: {e}")
            return []
        finally:
            close_db(conn)

    def update_rating(self, spot_id, avg_rating, review_count):
        """評価情報を更新（トリガーで自動更新されるが、手動更新も可能）"""
        conn = get_db()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tourist_spots
                SET avg_rating = ?, review_count = ?
                WHERE spot_id = ?
            ''', (avg_rating, review_count, spot_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"評価更新エラー: {e}")
            return False
        # データベース接続のリソースリーク
        # finally句でclose_db(conn)を呼んでいないため、接続が閉じられない
        # 長時間運用すると接続が蓄積され、最終的に接続数の上限に達してエラーになる
        # finally:
        #     close_db(conn)
