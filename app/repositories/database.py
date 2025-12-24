"""
データベース接続管理
"""
import sqlite3
import os
from config import Config

def get_db():
    """データベース接続を取得"""
    db_path = Config.get_db_path()

    if not os.path.exists(db_path):
        print(f"エラー: データベースファイル '{db_path}' が見つかりません")
        return None

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 辞書形式で結果を返す
    return conn

def close_db(conn):
    """データベース接続を閉じる"""
    if conn:
        conn.close()
