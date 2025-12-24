#!/usr/bin/env python3
"""
Level 2 - Issue A のテストスクリプト
問題: 統計ページの人気観光地ランキングで、順位が「0位」「1位」「2位」と表示されている
期待: ランキングは「1位」「2位」「3位」のように1から始まること
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_ranking_starts_from_one():
    """
    stats.htmlの人気観光地ランキングが1位から始まるかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # stats.htmlにアクセス
            page.goto('http://localhost:3001/stats.html', wait_until='networkidle')

            # 人気観光地ランキングのリストアイテムを取得
            ranking_items = page.locator('#topSpotsList .ranking-item')

            if ranking_items.count() == 0:
                print("❌ エラー: ランキングアイテムが見つかりません")
                browser.close()
                return False

            print(f"ランキングアイテムを {ranking_items.count()} 個見つけました\n")

            all_valid = True

            # 最初の3つのランキングをチェック
            for i in range(min(3, ranking_items.count())):
                item = ranking_items.nth(i)
                ranking_number = item.locator('.ranking-number').text_content().strip()
                spot_name = item.locator('.ranking-name').text_content().strip()

                print(f"ランキング {i+1}: {ranking_number} - {spot_name}")

                # 期待される順位
                expected_rank = f"{i+1}位"

                if ranking_number == expected_rank:
                    print(f"  ✅ 正しい順位です")
                elif ranking_number == f"{i}位":
                    print(f"  ❌ 0から始まっています（期待: {expected_rank}、実際: {ranking_number}）")
                    all_valid = False
                else:
                    print(f"  ⚠️  想定外の順位です（期待: {expected_rank}、実際: {ranking_number}）")
                    all_valid = False

            print()
            browser.close()

            if all_valid:
                print("✅ 合格: ランキングが1位から正しく始まっています")
                return True
            else:
                print("❌ 不合格: ランキングの順位表示に問題があります。Issue Aの「どうあるべきか」を確認してください。")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue A: ランキング順位の表示チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_ranking_starts_from_one()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
