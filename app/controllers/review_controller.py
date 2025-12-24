"""
レビューに関するエンドポイント
"""
from flask import Blueprint, request, jsonify
from services.review_service import ReviewService

review_bp = Blueprint('review', __name__)
review_service = ReviewService()

@review_bp.route('/reviews/<int:spot_id>', methods=['GET'])
def get_reviews(spot_id):
    """レビューを取得（観光地ID指定）"""
    try:
        reviews = review_service.get_reviews_by_spot(spot_id)
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@review_bp.route('/reviews', methods=['POST'])
def post_review():
    """レビューを投稿"""
    try:
        # FormDataで送信された場合とJSONで送信された場合の両方に対応
        if request.content_type and 'multipart/form-data' in request.content_type:
            # 画像付きレビューの場合
            result = review_service.create_review_with_photo(request)
        else:
            # JSON形式の場合（従来の実装）
            data = request.json
            if not data:
                return jsonify({'success': False, 'error': 'データが送信されていません'}), 400
            result = review_service.create_review(data)

        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """レビューを削除"""
    try:
        data = request.json
        if not data or 'user_id' not in data:
            return jsonify({'success': False, 'error': 'ユーザーIDが必要です'}), 400

        user_id = data['user_id']
        result = review_service.delete_review(review_id, user_id)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
