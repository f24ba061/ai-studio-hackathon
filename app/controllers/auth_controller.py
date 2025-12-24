"""
認証に関するエンドポイント
"""
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/auth', methods=['POST'])
def authenticate():
    """ユーザー認証"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'message': 'データが送信されていません'
            }), 400

        user_id = data.get('user_id')
        password = data.get('password')

        result = auth_service.authenticate(user_id, password)

        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/users', methods=['POST'])
def register_user():
    """ユーザー登録"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'データが送信されていません'
            }), 400

        result = auth_service.register_user(data)

        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
