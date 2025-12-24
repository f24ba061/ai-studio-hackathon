"""
統計データのコントローラー
"""
from flask import Blueprint, jsonify, request
from services.stats_service import StatsService

stats_bp = Blueprint('stats', __name__)
stats_service = StatsService()

@stats_bp.route('/stats/summary', methods=['GET'])
def get_summary():
    """基本統計情報を取得"""
    try:
        summary = stats_service.get_summary()
        return jsonify(summary), 200
    except Exception as e:
        print(f"基本統計取得エラー: {e}")
        return jsonify({'error': '統計情報の取得に失敗しました'}), 500

@stats_bp.route('/stats/spots-by-area', methods=['GET'])
def get_spots_by_area():
    """地域別観光地数を取得"""
    try:
        # オプションで特定地域のみ取得可能（バグ: SQLインジェクション脆弱性あり）
        area = request.args.get('area')
        areas = stats_service.get_spots_by_area(area)
        return jsonify(areas), 200
    except Exception as e:
        print(f"地域別統計取得エラー: {e}")
        return jsonify({'error': '地域別統計の取得に失敗しました'}), 500

@stats_bp.route('/stats/events-by-month', methods=['GET'])
def get_events_by_month():
    """月別イベント数を取得"""
    try:
        months = stats_service.get_events_by_month()
        return jsonify(months), 200
    except Exception as e:
        print(f"月別イベント統計取得エラー: {e}")
        return jsonify({'error': '月別イベント統計の取得に失敗しました'}), 500

@stats_bp.route('/stats/top-spots', methods=['GET'])
def get_top_spots():
    """人気観光地ランキングを取得"""
    try:
        limit = request.args.get('limit', 5)
        spots = stats_service.get_top_spots(limit)
        return jsonify(spots), 200
    except Exception as e:
        print(f"人気観光地ランキング取得エラー: {e}")
        return jsonify({'error': '人気観光地ランキングの取得に失敗しました'}), 500
