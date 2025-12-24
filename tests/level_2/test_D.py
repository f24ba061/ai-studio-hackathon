#!/usr/bin/env python3
"""
Level 2 - Issue D のテストスクリプト
問題: 観光地詳細ページの平均評価が小数点以下が長すぎる（例: 4.666666667）
期待: 平均評価は小数点第1位まで表示されること（例: 4.7）
"""

import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_rating_decimal_format():
    """
    spot-detail.htmlの平均評価が小数点第1位まで表示されているかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            print("複数の観光地で小数点表示をチェックします...\n")

            all_valid = True
            checked_count = 0

            # spot_id 1〜20 をテスト
            for spot_id in range(1, 21):
                page.goto(f'http://localhost:3001/spot-detail.html?id={spot_id}', wait_until='networkidle')

                # 平均評価表示を取得
                rating_element = page.locator('#spotRating')

                if rating_element.count() == 0:
                    continue

                rating_text = rating_element.text_content()

                # 数値部分を抽出
                match = re.search(r'[⭐★☆]\s*([\d.]+)', rating_text)

                if not match:
                    continue

                rating_value = match.group(1)

                # 小数点以下がある場合のみチェック
                if '.' in rating_value:
                    decimal_part = rating_value.split('.')[1]
                    decimal_length = len(decimal_part)

                    checked_count += 1
                    spot_name_element = page.locator('h1')
                    spot_name = spot_name_element.text_content().strip() if spot_name_element.count() > 0 else f"spot_id={spot_id}"

                    if decimal_length > 1:
                        print(f"{spot_name}: 評価 {rating_value}")
                        print(f"  ❌ 小数点以下が{decimal_length}桁です（期待: 1桁）")
                        all_valid = False
                    else:
                        print(f"{spot_name}: 評価 {rating_value}")
                        print(f"  ✅ 小数点第1位まで正しく表示されています")

                    # 5件チェックしたら終了
                    if checked_count >= 5:
                        break

            print()
            browser.close()

            if checked_count == 0:
                print("❌ エラー: 評価のある観光地が見つかりませんでした")
                return False

            if all_valid:
                print("✅ 合格: 平均評価が小数点第1位まで正しく表示されています")
                return True
            else:
                print("❌ 不合格: 平均評価の小数点表示に問題があります")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue D: 平均評価の小数点表示チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_rating_decimal_format()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("平均評価が小数点第1位まで正しく表示されています。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("平均評価の小数点表示に問題があります。")
        print(".toFixed(1) を使用して小数点第1位まで表示してください。")
        print("Issue Dの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
