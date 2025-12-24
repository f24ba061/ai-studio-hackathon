#!/usr/bin/env python3
"""
Level 3 - Issue C のテストスクリプト
問題: ログアウト後もレビュー投稿フォームが表示されてしまう
期待: ログアウト後はレビューフォームを非表示にし、ログイン通知を表示すること
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_review_form_after_logout():
    """
    ログアウト後にレビューフォームが非表示になるかをチェック（Playwright）
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # spot-detail.htmlにアクセス
            page.goto('http://localhost:3001/spot-detail.html?id=1', wait_until='networkidle')
            page.wait_for_timeout(1000)

            # まずログイン状態を確認
            login_button = page.locator('button:has-text("ログイン")')
            logout_button = page.locator('button:has-text("ログアウト")')

            # ログイン状態なら一旦ログアウト
            if logout_button.count() > 0:
                logout_button.click()
                page.wait_for_timeout(500)

            # ログアウト状態でのフォーム表示をチェック
            review_form = page.locator('#reviewForm')
            login_notice = page.locator('#loginNotice')

            is_form_visible = review_form.is_visible() if review_form.count() > 0 else False
            is_notice_visible = login_notice.is_visible() if login_notice.count() > 0 else False

            print("ログアウト状態での表示チェック:")
            print(f"  レビューフォーム: {'表示' if is_form_visible else '非表示'}")
            print(f"  ログイン通知: {'表示' if is_notice_visible else '非表示'}")
            print()

            browser.close()

            if not is_form_visible and is_notice_visible:
                print("✅ 合格: ログアウト後はレビューフォームが非表示になっています")
                return True
            elif is_form_visible:
                print("❌ 不合格: ログアウト後もレビューフォームが表示されています。Issue Cの「どうあるべきか」を確認してください。")
                return False
            else:
                print("⚠️  フォームは非表示ですが、ログイン通知も表示されていません")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def test_review_form_after_login():
    """
    ログイン状態でレビューフォームが表示されるかをチェック（Playwright）
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
            page.wait_for_timeout(1000)

            print("テストユーザーでログイン状態をシミュレート")

            # ログイン状態でのフォーム表示をチェック
            review_form = page.locator('#reviewForm')
            login_notice = page.locator('#loginNotice')

            is_form_visible = review_form.is_visible() if review_form.count() > 0 else False
            is_notice_visible = login_notice.is_visible() if login_notice.count() > 0 else False

            # テスト後にlocalStorageをクリア
            page.evaluate("localStorage.removeItem('currentUser');")

            print("ログイン状態での表示チェック:")
            print(f"  レビューフォーム: {'表示' if is_form_visible else '非表示'}")
            print(f"  ログイン通知: {'表示' if is_notice_visible else '非表示'}")
            print()

            browser.close()

            if is_form_visible and not is_notice_visible:
                print("✅ 合格: ログイン状態ではレビューフォームが表示されています")
                return True
            elif not is_form_visible:
                print("❌ 不合格: ログイン状態なのにレビューフォームが表示されていません")
                print("   loadUserFromStorage()がページ読み込み時に呼び出されているか確認してください")
                return False
            else:
                print("⚠️  フォームは表示されていますが、ログイン通知も表示されています")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue C: ログイン状態によるレビューフォーム表示制御チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    # テスト1: ログアウト状態でフォームが非表示になるか
    print("\n【テスト1: ログアウト状態のチェック】")
    logout_result = test_review_form_after_logout()

    # テスト2: ログイン状態でフォームが表示されるか
    print("\n【テスト2: ログイン状態のチェック】")
    login_result = test_review_form_after_login()

    # 両方のテストに合格する必要がある
    result = logout_result and login_result

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        print()
        print("ログイン状態によるフォーム表示制御が正しく実装されています。")
        print("- ログイン時: フォーム表示")
        print("- ログアウト時: フォーム非表示、ログイン通知表示")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        print()
        if not logout_result:
            print("- ログアウト状態でのフォーム非表示が正しく動作していません")
        if not login_result:
            print("- ログイン状態でのフォーム表示が正しく動作していません")
            print("  → loadUserFromStorage()がページ読み込み時に呼び出されているか確認してください")
        print()
        print("Issue Cの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
