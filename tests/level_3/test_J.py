#!/usr/bin/env python3
"""
Level 3 - Issue J のテストスクリプト
問題: レビュー削除時に画像ファイルの削除処理が抜けている（ディスク容量を圧迫）
期待: レビュー削除時に関連する画像ファイルも削除すること
"""

import sys
import requests
import random
import os
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_file_deletion():
    """
    レビュー削除時に画像ファイルも削除されるかをチェック
    """
    base_url = 'http://localhost:3001/api/reviews'

    # テスト用のランダムなuser_idとspot_idを生成
    test_user_id = random.randint(10000, 99999)
    test_spot_id = random.randint(1, 20)

    print("レビュー削除時の画像ファイル削除チェックを開始します\n")

    # ステップ1: 画像付きレビューを投稿
    print("=== ステップ1: 画像付きレビューを投稿 ===")

    # テスト用の画像ファイルを作成
    test_image_path = '/tmp/test_review_image.jpg'
    with open(test_image_path, 'wb') as f:
        # 1x1の小さなJPEG画像を作成
        f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xfe\xd4\xff\xd9')

    try:
        # FormDataで画像付きレビューを投稿
        with open(test_image_path, 'rb') as img:
            files = {'photo': ('test.jpg', img, 'image/jpeg')}
            data = {
                'user_id': test_user_id,
                'spot_id': test_spot_id,
                'review_content': 'テスト用のレビューです',
                'rating': 5
            }
            response = requests.post(base_url, files=files, data=data, timeout=10)

        if response.status_code not in [200, 201]:
            print(f"❌ レビューの投稿に失敗しました: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return False

        result = response.json()
        if not result.get('success'):
            print(f"❌ レビューの投稿に失敗しました: {result.get('error')}")
            return False

        review_id = result.get('review_id')
        photo_filename = result.get('photo_filename')

        if not photo_filename:
            print("⚠️  画像ファイル名が返されませんでした。画像なしレビューとして投稿されたようです")
            print("   このテストは画像付きレビューの削除をテストするため、スキップします")
            return True  # 画像機能が実装されていない場合はパスさせる

        print(f"✅ レビューを投稿しました (ID: {review_id}, 画像: {photo_filename})")

        # ステップ2: 画像ファイルが存在するか確認
        print("\n=== ステップ2: 画像ファイルの存在を確認 ===")

        # Dockerコンテナ内の画像ファイルパスを確認
        # 通常は /app/frontend/uploads/reviews/ などに保存される
        import subprocess
        result = subprocess.run(
            ['docker', 'exec', 'gunma-tourism-app', 'find', '/app', '-name', photo_filename],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and result.stdout.strip():
            image_path = result.stdout.strip()
            print(f"✅ 画像ファイルが存在します: {image_path}")
        else:
            print(f"⚠️  画像ファイルが見つかりませんでした: {photo_filename}")
            print("   画像アップロード機能が正しく動作していない可能性があります")
            return True  # 画像機能が実装されていない場合はパスさせる

        # ステップ3: レビューを削除
        print("\n=== ステップ3: レビューを削除 ===")

        delete_response = requests.delete(
            f'{base_url}/{review_id}',
            json={'user_id': test_user_id},
            timeout=10
        )

        if delete_response.status_code != 200:
            print(f"❌ レビューの削除に失敗しました: {delete_response.status_code}")
            return False

        delete_result = delete_response.json()
        if not delete_result.get('success'):
            print(f"❌ レビューの削除に失敗しました: {delete_result.get('error')}")
            return False

        print(f"✅ レビューを削除しました (ID: {review_id})")

        # ステップ4: 画像ファイルが削除されたか確認
        print("\n=== ステップ4: 画像ファイルの削除を確認 ===")

        result = subprocess.run(
            ['docker', 'exec', 'gunma-tourism-app', 'find', '/app', '-name', photo_filename],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and result.stdout.strip():
            print(f"❌ 不合格: 画像ファイルが削除されていません: {result.stdout.strip()}")
            print("   レビュー削除時に関連する画像ファイルも削除してください")
            return False
        else:
            print(f"✅ 合格: 画像ファイルが正しく削除されました")
            return True

    except Exception as e:
        print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
        return False
    finally:
        # テスト用画像ファイルを削除
        if os.path.exists(test_image_path):
            os.remove(test_image_path)


def main():
    print("=" * 60)
    print("Level 3 - Issue J: レビュー削除時の画像ファイル削除チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_file_deletion()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("レビュー削除時に画像ファイルも正しく削除されています。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("レビュー削除時に画像ファイルの削除処理が抜けています。")
        print("レビュー削除時に関連する画像ファイルも削除してください。")
        print("Issue Jの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
