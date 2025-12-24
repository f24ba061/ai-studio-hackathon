#!/usr/bin/env python3
"""
Level 3 - Issue E のテストスクリプト
問題: レビュー投稿フォームで、JavaScriptによるレビュー内容のバリデーションが実装されていない
期待: レビュー内容が空白または空白スペースのみの場合、エラーメッセージを表示すること
"""

import sys
from playwright.sync_api import sync_playwright


def test_review_text_validation():
    """
    レビュー投稿フォームでレビュー内容が空白の場合にバリデーションが動作するかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # spot-detail.htmlにアクセス
            page.goto('http://localhost:3001/spot-detail.html?id=1', wait_until='networkidle')

            # localStorageにテストユーザー情報を設定してログイン状態にする
            page.evaluate("""
                localStorage.setItem('currentUser', JSON.stringify({
                    user_id: 1,
                    name: 'テストユーザー'
                }));
            """)

            # ページをリロードしてログイン状態を反映
            page.reload(wait_until='networkidle')

            print("テストユーザーでログインしました")

            # レビューフォームが表示されるか確認
            review_form = page.locator('#reviewForm')

            if review_form.count() == 0:
                print("❌ エラー: レビューフォームが見つかりませんでした")
                browser.close()
                return False

            print("✅ レビューフォームを見つけました")

            # レビューセクションまでスクロール
            page.evaluate("document.querySelector('#reviewForm').scrollIntoView()")
            page.wait_for_timeout(500)

            # 名前を入力
            page.fill('#reviewerName', 'テストユーザー')

            # 星評価を設定（バリデーションが星評価だけでなくレビュー内容もチェックするため）
            star_buttons = page.locator('.star-rating .star')
            if star_buttons.count() > 0:
                star_buttons.nth(4).click()  # 5つ星を選択
                print("星評価を5に設定しました")

            # レビューテキストに空白スペースのみを入力
            review_text = page.locator('#reviewText')
            review_text.fill('   ')  # 空白スペースのみ

            print("レビューテキストに空白スペースのみを入力しました")

            # ダイアログ（alert）をキャプチャ
            dialog_message = None

            def handle_dialog(dialog):
                nonlocal dialog_message
                dialog_message = dialog.message
                dialog.accept()

            page.on('dialog', handle_dialog)

            # 投稿ボタンをクリック
            submit_button = page.locator('#reviewForm button[type="submit"]')
            submit_button.click()
            page.wait_for_timeout(1000)

            browser.close()

            # アラートが表示されたかチェック
            if dialog_message:
                print(f"✅ アラートが表示されました: 「{dialog_message}」")
                # レビュー内容に関するメッセージかチェック
                if 'レビュー' in dialog_message or '内容' in dialog_message or '入力' in dialog_message or '空' in dialog_message:
                    print("✅ 合格: レビュー内容のバリデーションが正しく動作しています")
                    return True
                else:
                    print("⚠️  アラートは表示されましたが、レビュー内容に関するメッセージではありませんでした")
                    return False
            else:
                print("❌ 不合格: 空白スペースのみでもアラートが表示されませんでした")
                print("   JavaScriptバリデーションが実装されていない可能性があります")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue E: レビュー内容バリデーションチェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_review_text_validation()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("レビュー内容のバリデーションが正しく実装されています。")
        print("レビュー内容が空白またはスペースのみの場合、エラーメッセージが表示されます。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("レビュー内容のバリデーションに問題があります。")
        print("レビュー内容が空白またはスペースのみの場合、JavaScriptでエラーメッセージを表示してください。")
        print("Issue Eの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
