"""
イベントのビジネスロジック
"""
from repositories.event_repository import EventRepository

class EventService:
    """イベントに関するビジネスロジック"""

    def __init__(self):
        self.event_repo = EventRepository()

    def get_all_events(self):
        """全イベントを取得"""
        return self.event_repo.find_all()

    def get_events_by_month(self, month):
        """月別でイベントを取得"""
        return self.event_repo.find_by_month(month)

    def get_events_by_area(self, area):
        """地域別でイベントを取得"""
        return self.event_repo.find_by_area(area)

    def search_events(self, keyword):
        """キーワードでイベントを検索"""
        return self.event_repo.find_by_keyword(keyword)
