"""
観光地に関するエンドポイント
"""
from flask import Blueprint, jsonify, request
from services.spot_service import SpotService

spot_bp = Blueprint('spot', __name__)
spot_service = SpotService()

@spot_bp.route('/spots', methods=['GET'])
def get_spots():
    """観光地一覧を取得"""
    try:
        spots = spot_service.get_all_spots()
        return jsonify(spots)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@spot_bp.route('/spots/search', methods=['GET'])
def search_spots():
    """観光地を検索"""
    try:
        keyword = request.args.get('keyword', '')
        if not keyword:
            return jsonify({'error': 'キーワードが指定されていません'}), 400

        spots = spot_service.search_spots(keyword)
        return jsonify(spots)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@spot_bp.route('/spots/<int:spot_id>', methods=['GET'])
def get_spot(spot_id):
    """特定の観光地を取得"""
    try:
        spot = spot_service.get_spot_by_id(spot_id)
        if spot:
            return jsonify(spot)
        else:
            return jsonify({'error': '観光地が見つかりません'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@spot_bp.route('/spots/nearby', methods=['GET'])
def get_nearby_spots():
    """近隣の観光地を取得"""
    try:
        # クエリパラメータから緯度経度を取得（実際には使わないが、APIの形式として受け取る）
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)

        # 近隣の観光地を取得
        spots = spot_service.get_nearby_spots(lat, lon)

        # Content-Typeヘッダーにcharsetを明示的に指定
        response = jsonify(spots)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500
