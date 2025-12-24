#!/usr/bin/env python3
"""
Level 3 - Issue F のテストスクリプト
問題: レビュー内容の文字数制限チェックがない（10万文字でも投稿可能）
期待: レビュー内容の文字数を制限し（例: 1000文字）、超えた場合はエラーを返すこと
"""

import sys
import requests
import random


def test_review_length_limit():
    """
    レビュー投稿APIで文字数制限が実装されているかをチェック
    """
    base_url = 'http://localhost:3001/api/reviews'

    print("レビュー内容の文字数制限チェックを開始します\n")

    # テスト用の非常に長いレビュー内容（10万文字）
    very_long_review = 'あ' * 100000

    # 正常な長さのレビュー内容
    normal_review = 'とても良かったです。また来たいと思います。'

    # 重複エラーを避けるため、ランダムなuser_idとspot_idを使用
    test_user_id = random.randint(1000, 9999)
    test_spot_id_1 = random.randint(1, 20)
    test_spot_id_2 = random.randint(1, 20)
    while test_spot_id_2 == test_spot_id_1:
        test_spot_id_2 = random.randint(1, 20)

    print("=== 長すぎるレビューのテスト（10万文字） ===")
    try:
        response = requests.post(base_url, json={
            'user_id': test_user_id,
            'spot_id': test_spot_id_1,
            'review_content': very_long_review,
            'rating': 5
        }, timeout=10)

        if response.status_code >= 400:
            data = response.json()
            error_msg = data.get('error', '')
            # 文字数制限エラーかチェック
            if '文字' in error_msg or '長' in error_msg or 'length' in error_msg.lower():
                print(f"✅ 文字数制限エラーを返しました: {error_msg}")
                long_review_rejected = True
            else:
                print(f"⚠️  エラーが返されましたが、文字数制限エラーではありません: {error_msg}")
                long_review_rejected = False
        elif response.status_code in [200, 201]:
            data = response.json()
            if data.get('success') == False:
                error_msg = data.get('error', '')
                if '文字' in error_msg or '長' in error_msg:
                    print(f"✅ 文字数制限エラーを返しました: {error_msg}")
                    long_review_rejected = True
                else:
                    print(f"⚠️  エラーレスポンスですが、文字数制限エラーではありません: {error_msg}")
                    long_review_rejected = False
            else:
                print("❌ 長すぎるレビューが受け入れられてしまいました")
                long_review_rejected = False
        else:
            print(f"❌ 予期しないステータスコード {response.status_code}")
            long_review_rejected = False

    except requests.exceptions.RequestException as e:
        print(f"❌ リクエストエラー: {e}")
        long_review_rejected = False

    print()
    print("=== 正常な長さのレビューのテスト ===")
    try:
        response = requests.post(base_url, json={
            'user_id': test_user_id,
            'spot_id': test_spot_id_2,
            'review_content': normal_review,
            'rating': 5
        }, timeout=10)

        if response.status_code in [200, 201]:
            data = response.json()
            if data.get('success') == True or 'review_id' in data:
                print("✅ 正常なレビューが受け入れられました")
                normal_review_accepted = True
            else:
                print(f"❌ 正常なレビューが拒否されました: {data}")
                normal_review_accepted = False
        else:
            print(f"❌ エラーステータス {response.status_code} を返しました")
            normal_review_accepted = False

    except requests.exceptions.RequestException as e:
        print(f"❌ リクエストエラー: {e}")
        normal_review_accepted = False

    print()

    if long_review_rejected and normal_review_accepted:
        print("✅ 合格: レビュー内容の文字数制限が正しく実装されています")
        return True
    else:
        print("❌ 不合格: レビュー内容の文字数制限に問題があります")
        if not long_review_rejected:
            print("   長すぎるレビュー（10万文字）が拒否されていません")
        if not normal_review_accepted:
            print("   正常な長さのレビューが受け入れられていません")
        return False


def main():
    print("=" * 60)
    print("Level 3 - Issue F: レビュー内容の文字数制限チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_review_length_limit()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("レビュー内容の文字数制限が正しく実装されています。")
        print("長すぎるレビューは拒否され、正常な長さのレビューは受け入れられます。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("レビュー内容の文字数制限が実装されていません。")
        print("レビュー内容の文字数を制限し（例: 1000文字）、超えた場合はエラーを返してください。")
        print("Issue Fの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
