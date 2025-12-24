#!/usr/bin/env python3
"""
Level 3 - Issue G のテストスクリプト
問題: 平均評価がNULLの場合のチェックがなく、round()実行時にエラーが発生する
期待: NULLチェックを行い、NULLの場合は0または適切なデフォルト値を設定すること
"""

import sys
import sqlite3
from playwright.sync_api import sync_playwright


def test_null_handling():
    """
    レビューを全削除してから/api/statsにアクセスし、
    平均評価がNULLの場合でもエラーが発生しないかをチェック
    """
    db_path = '/app/data/tourism_review.db'
    backup_reviews = []

    with sync_playwright() as p:
        # APIテスト用のrequestコンテキストを作成
        request_context = p.request.new_context(base_url='http://localhost:3001')

        try:
            # 1. レビューをバックアップして全削除
            print("レビューデータを一時的に削除しています...")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # 削除前のレビュー数を保存
            cursor.execute('SELECT * FROM reviews')
            backup_reviews = cursor.fetchall()
            print(f"  削除前のレビュー数: {len(backup_reviews)}件")

            # レビューを全削除
            cursor.execute('DELETE FROM reviews')
            conn.commit()
            conn.close()
            print("  レビューを全削除しました")

            # 2. /api/stats/summaryにアクセス
            print("\n/api/stats/summary にアクセスしています...")
            response = request_context.get('/api/stats/summary')

            print(f"  ステータスコード: {response.status}")

            # 3. 結果を判定
            if response.status == 500:
                print("\n❌ 不合格: 500エラーが発生しました")
                print("   NULLハンドリングが実装されていません")
                print("   avg_rating_overallがNULLの時にround()がエラーになっています")
                result = False
            elif response.status == 200:
                data = response.json()
                print(f"  レスポンス: {data}")

                # avg_rating_overallが適切に処理されているか確認
                if 'avg_rating_overall' in data:
                    avg_rating = data['avg_rating_overall']
                    # 0 または数値であればOK
                    if avg_rating == 0 or (isinstance(avg_rating, (int, float)) and avg_rating >= 0):
                        print("\n✅ 合格: NULLハンドリングが正しく実装されています")
                        print(f"   avg_rating_overall = {avg_rating} (適切なデフォルト値)")
                        result = True
                    else:
                        print(f"\n❌ 不合格: avg_rating_overallが不正な値です: {avg_rating}")
                        result = False
                else:
                    print("\n❌ 不合格: avg_rating_overallがレスポンスに含まれていません")
                    result = False
            else:
                print(f"\n❌ 不合格: 予期しないステータスコード: {response.status}")
                result = False

            # 4. レビューデータを復元
            print("\nレビューデータを復元しています...")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            for review in backup_reviews:
                cursor.execute('''
                    INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', review)
            conn.commit()
            conn.close()
            print(f"  {len(backup_reviews)}件のレビューを復元しました")

            request_context.dispose()
            return result

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            # エラーが起きても復元を試みる
            try:
                if backup_reviews:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    for review in backup_reviews:
                        cursor.execute('INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?)', review)
                    conn.commit()
                    conn.close()
                    print(f"  {len(backup_reviews)}件のレビューを復元しました（エラー時）")
            except Exception as restore_error:
                print(f"  復元エラー: {restore_error}")

            request_context.dispose()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue G: 平均評価のNULLハンドリングチェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_null_handling()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("平均評価がNULLの場合のハンドリングが正しく実装されています。")
        print("レビューが0件でもエラーが発生しません。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("平均評価がNULLの場合のハンドリングに問題があります。")
        print("NULLチェックを行い、NULLの場合は0または適切なデフォルト値を設定してください。")
        print("Issue Gの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
