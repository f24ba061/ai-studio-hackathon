"""
イベントに関するエンドポイント
"""
from flask import Blueprint, jsonify, request
from services.event_service import EventService

event_bp = Blueprint('event', __name__)
event_service = EventService()

@event_bp.route('/events', methods=['GET'])
def get_events():
    """イベント一覧を取得（フィルター対応）"""
    # エラーハンドリングが不十分（例外が発生するとスタックトレースが露出）
    # 本来はtry-exceptでエラーをキャッチして適切なエラーレスポンスを返すべき
    # try:
    # クエリパラメータを取得
    month = request.args.get('month')
    area = request.args.get('area')

    # フィルター適用
    if month:
        events = event_service.get_events_by_month(month)
    elif area:
        events = event_service.get_events_by_area(area)
    else:
        events = event_service.get_all_events()

    return jsonify(events)
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

@event_bp.route('/events/search', methods=['GET'])
def search_events():
    """イベントを検索"""
    # エラーハンドリングが不十分（例外が発生するとスタックトレースが露出）
    # try:
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({'error': 'キーワードが指定されていません'}), 400

    events = event_service.search_events(keyword)
    return jsonify(events)
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
