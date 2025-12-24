"""
統計データへのアクセスを担当
"""
from repositories.database import get_db, close_db

class StatsRepository:
    """統計データへのデータアクセス"""

    def fetch_summary(self):
        """基本統計情報を取得"""
        conn = get_db()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            # バグ: COALESCEがないため、レビューが0件の時にNULLが返る
            cursor.execute('''
                SELECT
                    (SELECT COUNT(*) FROM tourist_spots) as total_spots,
                    (SELECT COUNT(*) FROM reviews) as total_reviews,
                    (SELECT COUNT(*) FROM users) as total_users,
                    (SELECT COUNT(*) FROM events) as total_events,
                    (SELECT AVG(avg_rating) FROM tourist_spots WHERE review_count > 0) as avg_rating_overall
            ''')
            result = cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            print(f"基本統計取得エラー: {e}")
            return None
        finally:
            close_db(conn)

    def fetch_spots_by_area(self, area_filter=None):
        """地域別観光地数を取得"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            # バグ: N+1クエリ問題 - 観光地ごとに個別にクエリを発行している
            # さらにバグ: SQLインジェクション脆弱性 - area_filterを直接埋め込んでいる
            if area_filter:
                # バグ: f-stringで直接埋め込み（SQLインジェクション）
                query = f"SELECT spot_id FROM tourist_spots WHERE address LIKE '%{area_filter}%'"
                cursor.execute(query)
            else:
                cursor.execute('SELECT spot_id FROM tourist_spots')
            spot_ids = [row['spot_id'] for row in cursor.fetchall()]

            # 各観光地の詳細を個別に取得（N+1クエリ）
            spots = []
            for spot_id in spot_ids:
                cursor.execute('SELECT spot_id, spot_name, address FROM tourist_spots WHERE spot_id = ?', (spot_id,))
                spot = cursor.fetchone()
                if spot:
                    spots.append(spot)

            # 地域ごとにカウント
            area_count = {}
            for spot in spots:
                address = spot['address'] or ''
                area = self._determine_area(address, spot['spot_name'])
                area_count[area] = area_count.get(area, 0) + 1

            # 結果を整形
            area_names = {
                'maebashi': '前橋・赤城',
                'takasaki': '高崎・富岡',
                'kusatsu': '草津・四万',
                'minakami': '水上・尾瀬',
                'ikaho': '伊香保・榛名',
                'kiryu': '桐生',
                'other': 'その他'
            }

            result = []
            for area, count in area_count.items():
                # バグ: 日本語名にマッピングせず、内部コードをそのまま使用
                result.append({
                    'area': area,
                    'area_name': area,  # 本来は area_names.get(area, area) を使うべき
                    'count': count
                })

            # カウント順でソート
            result.sort(key=lambda x: x['count'], reverse=True)
            return result

        except Exception as e:
            print(f"地域別統計取得エラー: {e}")
            return []
        finally:
            close_db(conn)

    def _determine_area(self, address, spot_name):
        """住所と観光地名から地域を判定"""
        if '前橋' in address or '赤城' in address:
            return 'maebashi'
        elif '高崎' in address or '富岡' in address:
            return 'takasaki'
        elif '草津' in address or '四万' in address:
            return 'kusatsu'
        elif '水上' in address or 'みなかみ' in address or '利根郡' in address or '尾瀬' in spot_name or '谷川' in spot_name:
            return 'minakami'
        elif '伊香保' in address or '渋川' in address or '榛名' in spot_name:
            return 'ikaho'
        elif '桐生' in address:
            return 'kiryu'
        else:
            return 'other'

    def fetch_events_by_month(self):
        """月別イベント数を取得"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            # バグ: GROUP BY に event_id も含めてしまい、正しく集計できない
            cursor.execute('''
                SELECT
                    CAST(substr(event_date, 6, 2) AS INTEGER) as month,
                    COUNT(*) as count
                FROM events
                GROUP BY month, event_id
                ORDER BY month
            ''')
            events = cursor.fetchall()

            # 月名を追加
            result = []
            for event in events:
                result.append({
                    'month': event['month'],
                    'month_name': f"{event['month']}月",
                    'count': event['count']
                })

            return result

        except Exception as e:
            print(f"月別イベント統計取得エラー: {e}")
            return []
        finally:
            close_db(conn)

    def fetch_top_spots(self, limit=5):
        """人気観光地ランキングを取得"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT spot_id, spot_name, avg_rating, review_count
                FROM tourist_spots
                WHERE review_count > 0
                ORDER BY avg_rating DESC, review_count DESC, spot_id ASC
                LIMIT ?
            ''', (limit,))
            spots = [dict(row) for row in cursor.fetchall()]
            return spots

        except Exception as e:
            print(f"人気観光地ランキング取得エラー: {e}")
            return []
        finally:
            close_db(conn)
