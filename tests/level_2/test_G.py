#!/usr/bin/env python3
"""
Level 2 - Issue G のテストスクリプト
問題: イベント検索機能を使った後、検索結果が何件見つかったかの情報が表示されない
期待: 検索結果件数が「〇〇件見つかりました」のように表示されること
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_search_result_count():
    """
    events.htmlの検索結果件数が表示されるかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # events.htmlにアクセス
            page.goto('http://localhost:3001/events.html', wait_until='networkidle')

            # 検索ボックスにキーワードを入力
            search_input = page.locator('#searchInput')
            search_input.fill('まつり')

            # 検索ボタンをクリック
            search_button = page.locator('button', has_text='検索')
            search_button.click()
            page.wait_for_timeout(1000)

            # 検索結果情報の表示を取得
            search_result_info = page.locator('#searchResultInfo')

            if search_result_info.count() == 0:
                print("❌ エラー: 検索結果情報の表示要素が見つかりません")
                browser.close()
                return False

            result_text = search_result_info.text_content().strip()
            print(f"検索結果情報: 「{result_text}」")

            # 結果件数が表示されているかチェック
            # パターン1: 「まつり」の検索結果: X件
            # パターン2: X件見つかりました
            if '件' in result_text and ('検索結果' in result_text or '見つかりました' in result_text):
                print("✅ 合格: 検索結果件数が正しく表示されています")
                browser.close()
                return True
            elif result_text == '' or result_text == 'キーワードを入力してください':
                print("❌ 不合格: 検索結果件数が表示されていません")
                browser.close()
                return False
            else:
                print("⚠️  想定外のメッセージが表示されています")
                browser.close()
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue G: 検索結果件数の表示チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_search_result_count()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        print("検索結果件数の表示に問題があります。Issue Gの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
