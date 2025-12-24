"""
画像付きレビューのサンプルデータを追加するスクリプト
"""
import sqlite3
import sys
from pathlib import Path

# プロジェクトのルートディレクトリを取得
ROOT_DIR = Path(__file__).parent.parent
DB_PATH = ROOT_DIR / 'data' / 'tourism_review.db'

def add_photo_review():
    """画像付きレビューを追加"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # spot_id=1（草津温泉）に画像付きレビューを追加
        # まず既存のレビューを確認
        cursor.execute('SELECT COUNT(*) FROM reviews WHERE spot_id = 1 AND photo_filename IS NOT NULL')
        count = cursor.fetchone()[0]

        if count > 0:
            print(f'✅ 既に画像付きレビューが {count} 件存在します')
            return

        # photo_filenameカラムが存在するか確認
        cursor.execute("PRAGMA table_info(reviews)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'photo_filename' not in columns:
            print('⚠️ photo_filenameカラムが存在しません。スキーマを更新する必要があります。')
            # カラムを追加
            cursor.execute('ALTER TABLE reviews ADD COLUMN photo_filename TEXT')
            print('✅ photo_filenameカラムを追加しました')

        # 画像付きレビューを追加
        cursor.execute('''
            INSERT INTO reviews (user_id, spot_id, review_content, rating, photo_filename)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            4,  # user_id: サンプルユーザー（user_id=1,2,3は既にspot_id=1にレビュー済み）
            1,  # spot_id: 草津温泉
            '湯畑の夜景が本当に美しかったです！写真を撮りましたが、実物の方がもっと素晴らしいです。',
            5,  # rating
            'sample-photo-1.png'  # photo_filename
        ))

        conn.commit()
        print('✅ 画像付きレビューを追加しました（spot_id=1, 草津温泉）')

        # 確認
        cursor.execute('SELECT review_id, user_id, rating, photo_filename FROM reviews WHERE photo_filename IS NOT NULL')
        reviews = cursor.fetchall()
        print(f'\n📸 画像付きレビュー一覧:')
        for review in reviews:
            print(f'  - Review ID: {review[0]}, User ID: {review[1]}, Rating: {review[2]}, Photo: {review[3]}')

        conn.close()

    except Exception as e:
        print(f'❌ エラーが発生しました: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    print('📸 画像付きレビューのサンプルデータを追加します...\n')
    add_photo_review()
    print('\n✅ 完了しました！')
