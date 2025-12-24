#!/usr/bin/env python3
"""
Level 2 - Issue J のテストスクリプト
問題: 画像拡大モーダルでESCキーを押してもモーダルが閉じない
期待: ESCキーを押すとモーダルが閉じること
"""

import sys
from playwright.sync_api import sync_playwright


def test_esc_key_closes_modal():
    """
    画像拡大モーダルでESCキーを押すとモーダルが閉じるかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # spot-detail.htmlにアクセス
            page.goto('http://localhost:3001/spot-detail.html?id=1', wait_until='networkidle')

            # レビューセクションまでスクロール
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)

            # レビューに画像があるか確認
            review_images = page.locator('.reviews-list img[onclick*="showImageModal"]')

            if review_images.count() == 0:
                print("❌ エラー: レビュー画像が見つかりませんでした")
                print("テストを実行するには、画像付きレビューが必要です")
                browser.close()
                return False

            print(f"レビュー画像を {review_images.count()} 個見つけました\n")

            # 最初の画像をクリックしてモーダルを開く
            review_images.first.click()
            page.wait_for_timeout(500)

            # モーダルが表示されているか確認
            modal = page.locator('#imageModal')

            if not modal.is_visible():
                print("❌ エラー: 画像をクリックしてもモーダルが表示されません")
                browser.close()
                return False

            print("✅ モーダルが表示されました")

            # ESCキーを押す
            print("ESCキーを押します...")
            page.keyboard.press('Escape')
            page.wait_for_timeout(500)

            # モーダルが閉じたか確認
            if modal.is_visible():
                print("❌ 不合格: ESCキーを押してもモーダルが閉じませんでした")
                browser.close()
                return False
            else:
                print("✅ 合格: ESCキーでモーダルが正しく閉じました")
                browser.close()
                return True

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue J: ESCキーでモーダルを閉じる機能チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_esc_key_closes_modal()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("ESCキーでモーダルが正しく閉じるようになっています。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("ESCキーでモーダルを閉じる機能に問題があります。")
        print("keydownイベントリスナーでEscapeキーを監視してください。")
        print("Issue Jの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
