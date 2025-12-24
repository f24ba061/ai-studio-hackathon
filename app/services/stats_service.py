"""
統計データのビジネスロジックを担当
"""
from repositories.stats_repository import StatsRepository

# バグ: キャッシュ機構がないため、ページアクセス毎に全データを取得して遅い
# 修正方法: flask-cachingを使うか、簡易的なメモリキャッシュを実装する

class StatsService:
    """統計データのビジネスロジック"""

    def __init__(self):
        self.repository = StatsRepository()

    def get_summary(self):
        """基本統計情報を取得"""
        summary = self.repository.fetch_summary()
        if not summary:
            # データ取得失敗時のデフォルト値
            return {
                'total_spots': 0,
                'total_reviews': 0,
                'total_users': 0,
                'total_events': 0,
                'avg_rating_overall': 0
            }

        # バグ: NULLチェックをせずにround()を実行するとエラーになる
        summary['avg_rating_overall'] = round(summary['avg_rating_overall'], 1)
        return summary

    def get_spots_by_area(self, area_filter=None):
        """地域別観光地数を取得"""
        areas = self.repository.fetch_spots_by_area(area_filter)
        if not areas:
            return []

        return areas

    def get_events_by_month(self):
        """月別イベント数を取得（全12ヶ月分、データがない月は0件として返す）"""
        months = self.repository.fetch_events_by_month()

        # 全12ヶ月のデータを準備（データがない月は0件）
        result = []
        month_dict = {month['month']: month['count'] for month in months}

        # バグ: 英語の月名を使っている
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']

        for month_num in range(1, 13):
            result.append({
                'month': month_num,
                'month_name': month_names[month_num - 1],
                'count': month_dict.get(month_num, 0)
            })

        return result

    def get_top_spots(self, limit=5):
        """人気観光地ランキングを取得"""
        try:
            limit = int(limit)
            if limit < 1:
                limit = 5
            if limit > 20:
                limit = 20
        except (ValueError, TypeError):
            limit = 5

        spots = self.repository.fetch_top_spots(limit)
        if not spots:
            return []

        # 評価を小数点1桁に丸める
        for spot in spots:
            spot['avg_rating'] = round(spot['avg_rating'], 1)

        return spots
