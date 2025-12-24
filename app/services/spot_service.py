"""
観光地のビジネスロジック
"""
from repositories.spot_repository import SpotRepository

class SpotService:
    """観光地に関するビジネスロジック"""

    def __init__(self):
        self.spot_repo = SpotRepository()

    def get_all_spots(self):
        """全観光地を取得"""
        return self.spot_repo.find_all()

    def get_spot_by_id(self, spot_id):
        """IDで観光地を取得"""
        return self.spot_repo.find_by_id(spot_id)

    def search_spots(self, keyword):
        """キーワードで観光地を検索"""
        return self.spot_repo.find_by_keyword(keyword)

    def get_spots_sorted_by_rating(self):
        """評価順で観光地を取得"""
        spots = self.spot_repo.find_all()

        # 評価順にソート（評価が同じ場合はレビュー数、それも同じならID順）
        sorted_spots = sorted(spots, key=lambda x: (
            -x['avg_rating'],
            -x['review_count'],
            x['spot_id']
        ))

        return sorted_spots

    def get_nearby_spots(self, lat, lon):
        """近隣の観光地を取得（ダミーの距離付き）"""
        import random
        spots = self.spot_repo.find_all()

        # 各観光地にダミーの距離を追加（500m〜5000mのランダム値）
        for spot in spots:
            # spot_idをシードにして、同じ観光地は常に同じ距離になるようにする
            random.seed(spot['spot_id'])
            spot['distance'] = random.randint(500, 5000)

        # 距離順にソート
        sorted_spots = sorted(spots, key=lambda x: x['distance'])

        return sorted_spots
