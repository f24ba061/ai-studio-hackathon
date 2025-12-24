#!/usr/bin/env python3
"""
Level 3 - Issue I のテストスクリプト
問題: イベントコントローラーでエラーハンドリングが不十分（例外発生時にスタックトレースが露出）
期待: try-exceptでエラーをキャッチして適切なエラーレスポンスを返すこと
"""

import sys
from playwright.sync_api import sync_playwright


def test_error_handling():
    """
    events.htmlで不正なパラメータを指定してエラーハンドリングが正しく動作するかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # JavaScriptエラーをキャプチャ
        js_errors = []
        def log_error(error):
            js_errors.append(str(error))
            print(f"JavaScript error: {error}")
        page.on('pageerror', log_error)

        # コンソールエラーもキャプチャ
        console_errors = []
        def log_console(msg):
            if msg.type == 'error':
                console_errors.append(msg.text)
                print(f"Console error: {msg.text}")
        page.on('console', log_console)

        try:
            # 不正な月パラメータでイベントページにアクセス
            print("不正な月パラメータでイベントページにアクセスしています...")
            page.goto('http://localhost:3001/events.html?month=invalid', wait_until='networkidle')

            # ページが読み込まれるまで待機
            page.wait_for_timeout(2000)

            # スタックトレースが露出していないかチェック
            page_content = page.content()

            # スタックトレースの典型的なパターン
            stack_trace_patterns = [
                'Traceback',
                'File "',
                'line ',
                '.py"',
                'raise ',
                'Exception:',
                'Error:',
                'at Object.',
                'at Function.'
            ]

            has_stack_trace = False
            for pattern in stack_trace_patterns:
                if pattern in page_content and ('python' in page_content.lower() or 'traceback' in page_content.lower()):
                    has_stack_trace = True
                    print(f"⚠️  スタックトレースのパターンを検出: {pattern}")
                    break

            # エラーメッセージが適切に処理されているか確認
            if has_stack_trace:
                print("❌ 不合格: スタックトレースがユーザーに露出しています")
                browser.close()
                return False

            # 適切なエラーメッセージが表示されているか確認
            error_elements = page.locator('.error-message, .alert, [role="alert"]')
            if error_elements.count() > 0:
                print("✅ 適切なエラーメッセージが表示されています")

            # ページが正常に表示されているか（エラーで停止していないか）
            events_container = page.locator('.events-container, .container, main')
            if events_container.count() > 0:
                print("✅ ページが正常に表示されました")
            else:
                print("⚠️  ページコンテナを確認できませんでしたが、スタックトレースは露出していません")

            browser.close()

            if not has_stack_trace:
                print("✅ 合格: エラーハンドリングが正しく実装されています")
                print("   不正なパラメータでもスタックトレースが露出しません")
                return True
            else:
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue I: エラーハンドリングチェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_error_handling()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("エラーハンドリングが正しく実装されています。")
        print("例外発生時にスタックトレースが露出しません。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("エラーハンドリングに問題があります。")
        print("try-exceptでエラーをキャッチして適切なエラーレスポンスを返してください。")
        print("Issue Iの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
