#!/usr/bin/env python3
"""
群馬県観光地レビューアプリ - Python Flask版サーバー（3層アーキテクチャ版）
学生配布用：Python3のみで動作

実行方法:
    pip3 install flask flask-cors
    cd app
    python3 app.py

ブラウザアクセス:
    http://127.0.0.1:3001
"""

from flask import Flask
from flask_cors import CORS
import os

from config import Config
from controllers.spot_controller import spot_bp
from controllers.review_controller import review_bp
from controllers.auth_controller import auth_bp
from controllers.event_controller import event_bp
from controllers.stats_controller import stats_bp
from controllers.static_controller import static_bp

# Flaskアプリケーションの作成
app = Flask(__name__)
app.config.from_object(Config)
# CORS設定が緩すぎる
# 全てのオリジン（*）からのアクセスを許可している
# 悪意のあるサイトからAPIを呼び出される可能性がある
# 本来は CORS(app, origins=['http://localhost:3001']) のように制限すべき
CORS(app)

# ブループリント（各コントローラー）を登録
# 静的ファイル配信は最初に登録（ルートパスを含む）
app.register_blueprint(static_bp)

# API エンドポイントは /api プレフィックスで登録
app.register_blueprint(spot_bp, url_prefix='/api')
app.register_blueprint(review_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(event_bp, url_prefix='/api')
app.register_blueprint(stats_bp, url_prefix='/api')

# ===== エラーハンドリング =====

@app.errorhandler(404)
def not_found(error):
    from flask import jsonify
    return jsonify({'error': 'ページが見つかりません'}), 404

@app.errorhandler(500)
def internal_error(error):
    from flask import jsonify
    return jsonify({'error': 'サーバーエラーが発生しました'}), 500

# ===== メイン実行部分 =====

if __name__ == '__main__':
    print('=' * 60)
    print('🚀 群馬県観光地レビューアプリ - Python Flask版')
    print('   (3層アーキテクチャ構成)')
    print('=' * 60)
    print()

    # データベースファイルの存在確認
    db_path = Config.get_db_path()
    if not os.path.exists(db_path):
        print('⚠️  データベースファイルが見つかりません')
        print('   最初に以下のコマンドを実行してください:')
        print('   python3 init_db.py')
        print('   python3 database/add_tourist_spots.py')
        print()
    else:
        print('✅ データベースファイルを確認しました')
        print()

    print('📍 サーバーが起動します...')
    print('   ブラウザで以下にアクセス:')
    print('   🌐 http://127.0.0.1:3001')
    print('   📋 観光地一覧: http://127.0.0.1:3001/spots.html')
    print()
    print('⭐ テスト用ログイン情報:')
    print('   ユーザーID: 1')
    print('   パスワード: test123')
    print()
    print('🛑 サーバーを停止するには: Ctrl + C')
    print('=' * 60)

    # Flask開発サーバーを起動
    app.run(
        debug=Config.DEBUG,
        port=Config.PORT,
        host=Config.HOST
    )
