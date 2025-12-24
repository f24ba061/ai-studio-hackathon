#!/usr/bin/env python3
"""
Level 2 - Issue C のテストスクリプト
問題: formatDistance関数でreturn文が抜けているため、undefinedを返してしまう
期待: 各分岐でreturn文を追加し、正しく距離文字列を返すこと
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_distance_format():
    """
    index.htmlの近隣観光地の距離が正しくフォーマットされているかをチェック
    """
    with sync_playwright() as p:
        # 位置情報の許可を最初から設定したコンテキストを作成
        browser = p.chromium.launch()
        context = browser.new_context(
            geolocation={'latitude': 36.5, 'longitude': 138.5},
            permissions=['geolocation']
        )
        page = context.new_page()

        try:
            # index.htmlにアクセス
            page.goto('http://localhost:3001/index.html', wait_until='networkidle')

            # 近くの観光地セクションまでスクロール
            nearby_section = page.locator('#nearbySpots')
            if nearby_section.count() > 0:
                nearby_section.scroll_into_view_if_needed()

            # 「近くの観光地を表示」ボタンをクリック
            nearby_button = page.locator('button:has-text("近くの観光地を表示")')
            if nearby_button.count() == 0:
                print("❌ エラー: '近くの観光地を表示'ボタンが見つかりません")
                browser.close()
                return False

            nearby_button.click()

            # 観光地リストが表示されるまで待機（位置情報取得とAPI呼び出しに時間がかかる）
            page.wait_for_selector('#nearby-results .nearby-spot-item', timeout=15000)

            # 表示された観光地の距離を取得
            distance_elements = page.locator('#nearby-results .nearby-spot-distance')

            if distance_elements.count() == 0:
                print("❌ エラー: 観光地の距離表示が見つかりません")
                browser.close()
                return False

            print(f"観光地を {distance_elements.count()} 個見つけました\n")

            all_valid = True

            # 各距離表示をチェック
            for i in range(min(5, distance_elements.count())):
                distance_text = distance_elements.nth(i).text_content().strip()
                spot_name = page.locator('#nearby-results .nearby-spot-name').nth(i).text_content().strip()

                print(f"観光地 {i+1}: {spot_name} - 距離: {distance_text}")

                # "undefined" が含まれていないかチェック
                if 'undefined' in distance_text.lower():
                    print(f"  ❌ 距離が 'undefined' と表示されています")
                    all_valid = False
                # 正しい形式（数字 + 'm' または 数字 + 'km'）かチェック
                elif distance_text.endswith('m') or distance_text.endswith('km'):
                    print(f"  ✅ 距離が正しくフォーマットされています")
                else:
                    print(f"  ❌ 距離の形式が正しくありません（期待: '○○m' または '○○km'）")
                    all_valid = False

            print()
            browser.close()

            if all_valid:
                print("✅ 合格: 距離が正しくフォーマットされています")
                return True
            else:
                print("❌ 不合格: 距離表示に問題があります。Issue Cの「どうあるべきか」を確認してください。")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue C: 距離フォーマット表示チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    success = test_distance_format()

    print()
    print("=" * 60)
    if success:
        print("✅ テスト合格")
        print()
        print("formatDistance関数が正しく修正されています。")
        print("距離が適切にフォーマットされて表示されます。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("距離が正しく表示されていません。")
        print("formatDistance関数のreturn文を確認してください。")
        print("Issue Cの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
