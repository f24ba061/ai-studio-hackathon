"""
静的ファイル配信
"""
from flask import Blueprint, send_file
from config import Config
import os

static_bp = Blueprint('static', __name__)

@static_bp.route('/')
def index():
    """トップページ"""
    try:
        file_path = os.path.join(Config.FRONTEND_DIR, 'index.html')
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except FileNotFoundError:
        return "<h1>エラー</h1><p>index.htmlが見つかりません</p>", 404
    except Exception as e:
        return f"<h1>エラー</h1><p>ファイル読み込みエラー: {e}</p>", 500

@static_bp.route('/<path:filename>')
def static_files(filename):
    """静的ファイル（HTML, CSS, JS, 画像）の配信"""
    # APIパスは除外（他のブループリントに任せる）
    if filename.startswith('api/'):
        from flask import abort
        abort(404)

    # セキュリティ: パス上で上位ディレクトリに移動することを防ぐ
    if '..' in filename:
        return "不正なパスです", 403

    try:
        file_path = os.path.join(Config.FRONTEND_DIR, filename)

        # 画像ファイルの場合はバイナリで送信
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico')):
            mimetype = 'image/png' if filename.endswith('.png') else 'image/jpeg'
            return send_file(file_path, mimetype=mimetype)

        # ファイルタイプに応じてContent-Typeを設定
        if filename.endswith('.html'):
            content_type = 'text/html; charset=utf-8'
        elif filename.endswith('.css'):
            content_type = 'text/css; charset=utf-8'
        elif filename.endswith('.js'):
            content_type = 'application/javascript; charset=utf-8'
        else:
            content_type = 'text/plain; charset=utf-8'

        # ファイルを読み込んで返す
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return content, 200, {'Content-Type': content_type}

    except FileNotFoundError:
        return f"<h1>404 Not Found</h1><p>ファイルが見つかりません: {filename}</p>", 404
    except Exception as e:
        return f"<h1>500 Server Error</h1><p>ファイル読み込みエラー: {e}</p>", 500
