"""
イベントデータへのアクセスを担当
"""
from repositories.database import get_db, close_db

class EventRepository:
    """イベントテーブルへのデータアクセス"""

    def find_all(self):
        """全イベントを取得"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM events ORDER BY event_date')
            events = [dict(row) for row in cursor.fetchall()]
            return events
        except Exception as e:
            print(f"イベント一覧取得エラー: {e}")
            return []
        finally:
            close_db(conn)

    def find_by_month(self, month):
        """月別でイベントを取得"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            # 月の範囲チェックがない（13月なども受け付ける）
            # 月の形式は "01", "02", ... "12"
            month_str = f'{int(month):02d}'
            cursor.execute('''
                SELECT * FROM events
                WHERE substr(event_date, 6, 2) = ?
                ORDER BY event_date
            ''', (month_str,))
            events = [dict(row) for row in cursor.fetchall()]
            return events
        except Exception as e:
            print(f"月別イベント取得エラー: {e}")
            return []
        finally:
            close_db(conn)

    def find_by_area(self, area):
        """地域別でイベントを取得"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM events
                WHERE area = ?
                ORDER BY event_date
            ''', (area,))
            events = [dict(row) for row in cursor.fetchall()]
            return events
        except Exception as e:
            print(f"地域別イベント取得エラー: {e}")
            return []
        finally:
            close_db(conn)

    def find_by_keyword(self, keyword):
        """キーワードでイベントを検索（イベント名、場所、説明から検索）"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            # SQLインジェクション脆弱性（文字列連結を使用）
            query = f'''
                SELECT * FROM events
                WHERE event_name LIKE '%{keyword}%'
                   OR location LIKE '%{keyword}%'
                   OR description LIKE '%{keyword}%'
                ORDER BY event_date
            '''
            cursor.execute(query)
            events = [dict(row) for row in cursor.fetchall()]
            return events
        except Exception as e:
            print(f"イベント検索エラー: {e}")
            return []
        finally:
            close_db(conn)
