from repositories.review_repository import ReviewRepository
from services.file_service import FileService

class ReviewService:
    """レビューに関するビジネスロジック"""

    def __init__(self):
        self.review_repo = ReviewRepository()
        self.file_service = FileService()

    def get_reviews_by_spot(self, spot_id):
        """観光地のレビューを取得（N+1問題解消済み）"""
        # リポジトリ層でJOIN済みのデータをそのまま取得
        return self.review_repo.find_by_spot_id(spot_id)

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
        return {'success': False, 'error': 'レビューの作成に失敗しました'}

    def create_review_with_photo(self, request):
        """レビューを作成（画像あり）"""
        user_id = request.form.get('user_id')
        spot_id = request.form.get('spot_id')
        review_content = request.form.get('review_content')
        rating = request.form.get('rating')
        photo = request.files.get('photo')

        if not all([user_id, spot_id, review_content, rating]):
            return {'success': False, 'error': '必須項目が不足しています'}

        existing_review = self.review_repo.find_by_user_and_spot(user_id, spot_id)
        if existing_review:
            return {'success': False, 'error': '既にレビューを投稿しています'}

        if photo and photo.filename:
            validation_error = self.file_service.validate_image(photo)
            if validation_error:
                return {'success': False, 'error': validation_error}

        review_id = self.review_repo.create({
            'user_id': user_id,
            'spot_id': spot_id,
            'review_content': review_content,
            'rating': rating
        })

        if not review_id:
            return {'success': False, 'error': 'レビューの作成に失敗しました'}

        photo_filename = None
        if photo and photo.filename:
            try:
                photo_filename = self.file_service.save_review_photo(photo, review_id)
                self.review_repo.update_photo_filename(review_id, photo_filename)
            except Exception as e:
                print(f"画像保存エラー: {e}")

        return {
            'success': True,
            'review_id': review_id,
            'photo_filename': photo_filename,
            'message': 'レビューを投稿しました'
        }

    def delete_review(self, review_id, user_id):
        """レビューを削除"""
        review = self.review_repo.find_by_id(review_id)
        if not review:
            return {'success': False, 'error': 'レビューが見つかりません'}

        if self.review_repo.delete(review_id):
            return {'success': True, 'message': 'レビューを削除しました'}

        return {'success': False, 'error': 'レビューの削除に失敗しました'}