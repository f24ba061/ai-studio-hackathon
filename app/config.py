"""
アプリケーション設定ファイル
"""
import os

class Config:
    """基本設定"""
    # プロジェクトルートディレクトリ（app/の親ディレクトリ）
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # データベース（data/配下に統一）
    DB_NAME = 'data/tourism_review.db'

    # サーバー設定
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')  # Dockerコンテナ内では0.0.0.0が必要
    PORT = int(os.environ.get('FLASK_PORT', 3001))
    DEBUG = os.environ.get('FLASK_ENV', 'development') == 'development'

    # ファイルアップロード設定（絶対パス）
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'frontend', 'assets', 'images', 'reviews')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

    # フロントエンド設定（絶対パス）
    FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

    @staticmethod
    def get_db_path():
        """データベースファイルのパスを取得（環境変数優先）"""
        # 環境変数DB_PATHが設定されていればそれを使用（Docker用）
        db_path = os.environ.get('DB_PATH')
        if db_path:
            return db_path
        # 環境変数がなければデフォルトのパス
        return os.path.join(Config.PROJECT_ROOT, Config.DB_NAME)
