#!/usr/bin/env python3
"""
Level 3 - Issue B のテストスクリプト
問題: 月パラメータのバリデーションがない（13月、0月なども受け付ける）
期待: 月は1〜12の範囲でバリデーションを行い、範囲外の場合はエラーを返すこと
"""

import sys
from playwright.sync_api import sync_playwright


def test_month_validation():
    """
    /api/events?month=XXX のエンドポイントで月のバリデーションが実装されているかをチェック
    """
    with sync_playwright() as p:
        # APIテスト用のrequestコンテキストを作成（ブラウザ不要）
        request_context = p.request.new_context(base_url='http://localhost:3001')

        try:
            print("月のバリデーション実装確認を開始します\n")

            # テストケース: 無効な月の値
            invalid_months = [0, 13, -1, 100, 999]
            # テストケース: 有効な月の値
            valid_months = [1, 6, 12]

            print("=== 無効な月のテスト ===")
            invalid_results = {}

            for month in invalid_months:
                try:
                    response = request_context.get(f'/api/events?month={month}')

                    # ステータスコードが200以外（エラー）であることを期待
                    if response.status == 200:
                        print(f"  月={month}: ❌ 200 OKを返してしまいました（バリデーションなし）")
                        invalid_results[month] = False
                    else:
                        print(f"  月={month}: ✅ エラーステータス ({response.status}) を返しました")
                        invalid_results[month] = True

                except Exception as e:
                    print(f"  月={month}: ❌ リクエストエラー: {e}")
                    invalid_results[month] = False

            print()
            print("=== 有効な月のテスト ===")
            valid_results = {}

            for month in valid_months:
                try:
                    response = request_context.get(f'/api/events?month={month}')

                    # ステータスコードが200で、配列を返すことを期待
                    if response.status == 200:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"  月={month}: ✅ 正常にデータを返しました（{len(data)}件）")
                            valid_results[month] = True
                        else:
                            print(f"  月={month}: ❌ 配列以外のデータを返しました")
                            valid_results[month] = False
                    else:
                        print(f"  月={month}: ❌ エラーステータス {response.status} を返しました")
                        valid_results[month] = False

                except Exception as e:
                    print(f"  月={month}: ❌ リクエストエラー: {e}")
                    valid_results[month] = False

            print()

            # すべての無効な月が拒否され、すべての有効な月が受け入れられればOK
            all_invalid_rejected = all(invalid_results.values())
            all_valid_accepted = all(valid_results.values())

            request_context.dispose()

            if all_invalid_rejected and all_valid_accepted:
                print("✅ 合格: 月のバリデーションが正しく実装されています")
                return True
            else:
                print("❌ 不合格: 月のバリデーションに問題があります")
                if not all_invalid_rejected:
                    print("   無効な月（0, 13など）が拒否されていません")
                if not all_valid_accepted:
                    print("   有効な月（1-12）が正しく処理されていません")
                print("   Issue Bの「どうあるべきか」を確認してください。")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            request_context.dispose()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue B: 月パラメータのバリデーションチェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_month_validation()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("月のバリデーションが正しく実装されています。")
        print("無効な月（0, 13など）は拒否され、有効な月（1-12）は受け入れられます。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("月のバリデーションが実装されていません。")
        print("1-12の範囲外の月は、エラーを返すようにしてください。")
        print("Issue Bの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
