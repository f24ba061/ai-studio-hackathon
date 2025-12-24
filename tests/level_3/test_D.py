#!/usr/bin/env python3
"""
Level 3 - Issue D のテストスクリプト
問題: レビュー投稿フォームで、JavaScriptによる星評価のバリデーションが実装されていない
期待: 星評価が0の場合、JavaScriptでエラーメッセージを表示して投稿を防ぐこと
"""

import sys
from playwright.sync_api import sync_playwright


def test_rating_validation():
    """
    レビュー投稿フォームで星評価0の場合にバリデーションが動作するかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # コンソールログをキャプチャ
        def log_console(msg):
            print(f"Console: {msg.text}")
        page.on('console', log_console)

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

            # 名前とレビューテキストを入力（星評価は0のまま）
            page.fill('#reviewerName', 'テストユーザー')
            review_text = page.locator('#reviewText')
            review_text.fill('テスト用のレビューです')

            print("レビューテキストを入力しました（星評価=0）")

            # 星評価が0のまま投稿ボタンをクリック
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
                # 星評価に関するメッセージかチェック
                if '星' in dialog_message or '評価' in dialog_message or 'rating' in dialog_message.lower():
                    print("✅ 合格: 星評価0のバリデーションが正しく動作しています")
                    return True
                else:
                    print("⚠️  アラートは表示されましたが、星評価に関するメッセージではありませんでした")
                    return False
            else:
                print("❌ 不合格: 星評価0でもアラートが表示されませんでした")
                print("   JavaScriptバリデーションが実装されていない可能性があります")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue D: 星評価バリデーションチェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_rating_validation()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("星評価0のバリデーションが正しく実装されています。")
        print("星評価が選択されていない場合、エラーメッセージが表示されます。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("星評価バリデーションに問題があります。")
        print("星評価が0の場合、JavaScriptでエラーメッセージを表示してください。")
        print("Issue Dの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
