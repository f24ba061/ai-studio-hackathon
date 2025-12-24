#!/usr/bin/env python3
"""
Level 2 - Issue B のテストスクリプト
問題: イベント一覧ページで、開催日が「2025-08-15」のようなデータベース形式で表示されている
期待: イベントの開催日が「8月」と「15」のように分かれて見やすく表示されること
"""

import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_event_date_format():
    """
    events.htmlのイベント日付が正しくフォーマットされているかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # events.htmlにアクセス
            page.goto('http://localhost:3001/events.html', wait_until='networkidle')

            # JavaScriptでイベントが動的に読み込まれるのを待つ
            page.wait_for_selector('.event-item', timeout=10000)

            # イベントアイテムを取得
            event_items = page.locator('.event-item')

            if event_items.count() == 0:
                print("❌ エラー: イベントアイテムが見つかりません")
                browser.close()
                return False

            print(f"イベントアイテムを {event_items.count()} 個見つけました\n")

            all_valid = True

            # 最初の3つのイベントをチェック
            for i in range(min(3, event_items.count())):
                item = event_items.nth(i)
                event_title = item.locator('h3').text_content().strip()

                # 日付ボックス内の月と日を取得
                date_month = item.locator('.event-month').text_content().strip()
                date_day = item.locator('.event-day').text_content().strip()

                print(f"イベント {i+1}: {event_title}")
                print(f"  月: 「{date_month}」")
                print(f"  日: 「{date_day}」")

                # データベース形式（YYYY-MM-DD）が含まれているかチェック
                db_format_pattern = r'\d{4}-\d{2}-\d{2}'

                if re.search(db_format_pattern, date_month) or re.search(db_format_pattern, date_day):
                    print(f"  ❌ データベース形式（YYYY-MM-DD）で表示されています")
                    all_valid = False
                elif date_month.endswith('月') and date_day.isdigit():
                    print(f"  ✅ 正しくフォーマットされています")
                else:
                    print(f"  ⚠️  想定外の形式です")
                    all_valid = False

                print()

            browser.close()

            if all_valid:
                print("✅ 合格: イベント日付が正しくフォーマットされています")
                return True
            else:
                print("❌ 不合格: イベント日付の表示に問題があります。Issue Bの「どうあるべきか」を確認してください。")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue B: イベント日付の表示形式チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_event_date_format()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
