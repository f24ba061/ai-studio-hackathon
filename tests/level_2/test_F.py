#!/usr/bin/env python3
"""
Level 2 - Issue F のテストスクリプト
問題: チェックイン機能で未来の日付を選択できてしまう
期待: 未来の日付を選択した場合、エラーメッセージを表示してチェックインを拒否すること
"""

import sys
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright


def test_future_date_validation():
    """
    index.htmlのチェックイン機能で未来の日付が拒否されるかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # index.htmlにアクセス
            page.goto('http://localhost:3001/index.html', wait_until='networkidle')

            # 人気の観光スポットセクションまでスクロール
            popular_section = page.locator('#popularSpots')
            if popular_section.count() > 0:
                popular_section.scroll_into_view_if_needed()

            # 最初の観光地カードのチェックイン機能をテスト
            # 訪問日入力フィールドを探す
            date_input = page.locator('input[type="date"]').first

            if date_input.count() == 0:
                print("❌ エラー: 訪問日の入力フィールドが見つかりません")
                browser.close()
                return False

            # 未来の日付を設定（明日）
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            date_input.fill(tomorrow)

            print(f"未来の日付を入力: {tomorrow}")

            # ダイアログ（アラート）をキャプチャ
            dialog_message = None
            def handle_dialog(dialog):
                nonlocal dialog_message
                dialog_message = dialog.message
                dialog.accept()

            page.on('dialog', handle_dialog)

            # チェックインボタンをクリック
            checkin_button = page.locator('button:has-text("ここに行った")').first
            if checkin_button.count() == 0:
                print("❌ エラー: チェックインボタンが見つかりません")
                browser.close()
                return False

            checkin_button.click()

            # 少し待機してダイアログを確認
            page.wait_for_timeout(1000)

            browser.close()

            # エラーメッセージが表示されたかチェック
            if dialog_message:
                print(f"\n表示されたメッセージ: {dialog_message}")

                if '未来の日付' in dialog_message or '選択できません' in dialog_message:
                    print("✅ 合格: 未来の日付が正しく拒否されました")
                    return True
                else:
                    print("❌ 不合格: エラーメッセージが期待と異なります")
                    print("期待されるメッセージ: 「未来の日付は選択できません」")
                    return False
            else:
                print("❌ 不合格: 未来の日付に対するエラーメッセージが表示されませんでした")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue F: チェックイン機能の日付バリデーション")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    success = test_future_date_validation()

    print()
    print("=" * 60)
    if success:
        print("✅ テスト合格")
        print()
        print("チェックイン機能の日付バリデーションが正しく実装されています。")
        print("未来の日付を選択した場合、エラーメッセージが表示されます。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("日付バリデーションが不足しています。")
        print("未来の日付を選択した場合、「未来の日付は選択できません」と表示してください。")
        print("Issue Fの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
