"""
認証のビジネスロジック
"""
from repositories.user_repository import UserRepository

class AuthService:
    """認証に関するビジネスロジック"""

    def __init__(self):
        self.user_repo = UserRepository()

    def authenticate(self, user_id, password):
        """ユーザー認証"""
        if not user_id or not password:
            return {
                'success': False,
                'message': 'ユーザーIDとパスワードを入力してください'
            }

        user = self.user_repo.find_by_credentials(user_id, password)

        if user:
            return {
                'success': True,
                'user': {
                    'user_id': user['user_id'],
                    'name': user['name']
                }
            }
        else:
            return {
                'success': False,
                'message': 'ユーザーIDまたはパスワードが正しくありません'
            }

    def register_user(self, user_data):
        """ユーザー登録"""
        if 'password' not in user_data or 'name' not in user_data:
            return {
                'success': False,
                'error': 'パスワードと名前を入力してください'
            }

        user_id = self.user_repo.create(user_data)

        if user_id:
            return {
                'success': True,
                'user_id': user_id,
                'message': 'ユーザーを登録しました'
            }
        else:
            return {
                'success': False,
                'error': 'ユーザー登録に失敗しました'
            }
