#!/usr/bin/env python3
"""
Level 2 - Issue I のテストスクリプト
問題: 地域フィルターボタンを複数回クリックすると、複数のボタンがアクティブになる
期待: 常に1つのボタンだけがアクティブになること
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_area_filter_single_active():
    """
    spots.htmlの地域フィルターボタンが1つだけアクティブになるかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # spots.htmlにアクセス
            page.goto('http://localhost:3001/spots.html', wait_until='networkidle')

            # 地域フィルターボタンを取得
            area_buttons = page.locator('.area-btn')

            if area_buttons.count() == 0:
                print("❌ エラー: 地域フィルターボタンが見つかりません")
                browser.close()
                return False

            print(f"地域フィルターボタン数: {area_buttons.count()}個")

            # 複数のボタンをクリックしてテスト
            test_sequence = [
                "前橋・赤城",
                "高崎・富岡",
                "水上・みなかみ"
            ]

            all_valid = True

            for button_text in test_sequence:
                # ボタンをクリック
                button = page.locator('.area-btn', has_text=button_text)
                if button.count() > 0:
                    button.click()
                    page.wait_for_timeout(500)  # クリック後の処理を待つ

                    # アクティブなボタンの数を確認
                    active_buttons = page.locator('.area-btn.active')
                    active_count = active_buttons.count()

                    print(f"\n「{button_text}」クリック後:")
                    print(f"  アクティブなボタン数: {active_count}個")

                    if active_count > 1:
                        print(f"  ❌ 複数のボタンがアクティブになっています")
                        # どのボタンがアクティブか表示
                        for i in range(active_count):
                            active_text = active_buttons.nth(i).text_content().strip()
                            print(f"    - {active_text}")
                        all_valid = False
                    elif active_count == 0:
                        print(f"  ⚠️  警告: アクティブなボタンがありません")
                        all_valid = False
                    else:
                        active_text = active_buttons.text_content().strip()
                        print(f"  ✅ アクティブ: {active_text}")

            browser.close()

            if all_valid:
                print("\n✅ 合格: 地域フィルターボタンは常に1つだけがアクティブです")
                return True
            else:
                print("\n❌ 不合格: 地域フィルターボタンのアクティブ状態に問題があります。Issue Iの「どうあるべきか」を確認してください。")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue I: 地域フィルターボタンのアクティブ状態チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_area_filter_single_active()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
