"""
レビューのビジネスロジック
"""
from repositories.review_repository import ReviewRepository
from services.file_service import FileService


class ReviewService:
    """レビューに関するビジネスロジック"""

    def __init__(self):
        self.review_repo = ReviewRepository()
        self.file_service = FileService()

    def get_reviews_by_spot(self, spot_id):
        """観光地のレビューを取得"""
        # N+1クエリ問題あり（改善余地）
        from repositories.user_repository import UserRepository
        user_repo = UserRepository()

        reviews = self.review_repo.find_by_spot_id(spot_id)

        for review in reviews:
            user = user_repo.find_by_id(review['user_id'])
            review['user_name'] = user['name'] if user else '不明'

        return reviews

    def create_review(self, review_data):
        """レビューを作成（画像なし）"""
        required_fields = ['user_id', 'spot_id', 'review_content', 'rating']
        for field in required_fields:
            if field not in review_data:
                return {'success': False, 'error': f'{field}が指定されていません'}

        existing_review = self.review_repo.find_by_user_and_spot(
            review_data['user_id'],
            review_data['spot_id']
        )
        if existing_review:
            return {
                'success': False,
                'error': 'この観光地には既にレビューを投稿済みです。'
            }

        review_id = self.review_repo.create(review_data)

        if review_id:
            return {
                'success': True,
                'review_id': review_id,
                'message': 'レビューを投稿しました'
            }
        else:
            return {'success': False, 'error': 'レビューの作成に失敗しました'}

    def create_review_with_photo(self, request):
        """レビューを作成（画像あり・トランザクション対応）"""

        user_id = request.form.get('user_id')
        spot_id = request.form.get('spot_id')
        review_content = request.form.get('review_content')
        rating = request.form.get('rating')
        photo = request.files.get('photo')

        # 必須項目チェック
        if not all([user_id, spot_id, review_content, rating]):
            return {'success': False, 'error': '必須項目が不足しています'}

        # 重複チェック
        existing_review = self.review_repo.find_by_user_and_spot(user_id, spot_id)
        if existing_review:
            return {
                'success': False,
                'error': 'この観光地には既にレビューを投稿済みです。'
            }

        # 画像バリデーション
        if photo and photo.filename:
            validation_error = self.file_service.validate_image(photo)
            if validation_error:
                return {'success': False, 'error': validation_error}

        review_id = None
        photo_filename = None

        try:
            # ===== トランザクション開始（疑似） =====

            # ① レビュー作成
            review_id = self.review_repo.create({
                'user_id': user_id,
                'spot_id': spot_id,
                'review_content': review_content,
                'rating': rating
            })

            if not review_id:
                raise Exception('レビュー作成に失敗しました')

            # ② 画像保存
            if photo and photo.filename:
                photo_filename = self.file_service.save_review_photo(photo, review_id)
                self.review_repo.update_photo_filename(review_id, photo_filename)

            # ===== トランザクション成功 =====

        except Exception as e:
            print(f"レビュー投稿エラー: {e}")

            # ===== ロールバック処理 =====
            if review_id:
                self.review_repo.delete(review_id)

            return {
                'success': False,
                'error': 'レビュー投稿中にエラーが発生しました'
            }

        return {
            'success': True,
            'review_id': review_id,
            'photo_filename': photo_filename,
            'message': 'レビューを投稿しました'
        }

    def delete_review(self, review_id, user_id):
        """レビューを削除（権限チェック付き：未対応）"""

        review = self.review_repo.find_by_id(review_id)

        if not review:
            return {'success': False, 'error': 'レビューが見つかりません'}

        # 本来必要な権限チェック（未実装）
        # if review['user_id'] != int(user_id):
        #     return {'success': False, 'error': '他のユーザーのレビューは削除できません'}

        # 本来必要な画像削除処理（未実装）
        # if review.get('photo_filename'):
        #     self.file_service.delete_review_photo(review['photo_filename'])

        if self.review_repo.delete(review_id):
            return {
                'success': True,
                'message': 'レビューを削除しました'
            }
        else:
            return {'success': False, 'error': 'レビューの削除に失敗しました'}