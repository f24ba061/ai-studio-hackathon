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
            cursor.execute('''
                SELECT
                    (SELECT COUNT(*) FROM tourist_spots) AS total_spots,
                    (SELECT COUNT(*) FROM reviews) AS total_reviews,
                    (SELECT COUNT(*) FROM users) AS total_users,
                    (SELECT COUNT(*) FROM events) AS total_events,
                    (SELECT AVG(avg_rating)
                     FROM tourist_spots
                     WHERE review_count > 0) AS avg_rating_overall
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

            if area_filter:
                # ※本来はSQLインジェクション対策が必要（今回は未修正）
                query = f"SELECT spot_id FROM tourist_spots WHERE address LIKE '%{area_filter}%'"
                cursor.execute(query)
            else:
                cursor.execute('SELECT spot_id FROM tourist_spots')

            spot_ids = [row['spot_id'] for row in cursor.fetchall()]

            spots = []
            for spot_id in spot_ids:
                cursor.execute(
                    'SELECT spot_id, spot_name, address FROM tourist_spots WHERE spot_id = ?',
                    (spot_id,)
                )
                spot = cursor.fetchone()
                if spot:
                    spots.append(spot)

            area_count = {}
            for spot in spots:
                address = spot['address'] or ''
                area = self._determine_area(address, spot['spot_name'])
                area_count[area] = area_count.get(area, 0) + 1

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
                result.append({
                    'area': area,
                    'area_name': area_names.get(area, area),
                    'count': count
                })

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
        """月別イベント数を取得（修正版）"""
        conn = get_db()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            # 修正ポイント：
            # GROUP BY から event_id を削除し、月単位で正しく集計する
            cursor.execute('''
                SELECT
                    CAST(substr(event_date, 6, 2) AS INTEGER) AS month,
                    COUNT(*) AS count
                FROM events
                GROUP BY month
                ORDER BY month
            ''')
            events = cursor.fetchall()

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
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"人気観光地ランキング取得エラー: {e}")
            return []
        finally:
            close_db(conn)