#!/usr/bin/env python3
"""
Level 2 - Issue E のテストスクリプト
問題: 人気ランキングの星評価の数が正しくない（5個を超える場合がある）
期待: 星の総数が常に5個以内であること
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_ranking_star_count():
    """
    spots.htmlの人気ランキング内の星評価が5個以内かをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # spots.htmlにアクセス
            page.goto('http://localhost:3001/spots.html', wait_until='networkidle')

            # 人気ランキングセクション内の全ての星評価を取得
            ranking_items = page.locator('#rankingList .ranking-item')

            if ranking_items.count() == 0:
                print("❌ エラー: 人気ランキングが見つかりません")
                browser.close()
                return False

            all_valid = True
            for i in range(ranking_items.count()):
                item = ranking_items.nth(i)
                spot_name = item.locator('.ranking-name a').text_content().strip()
                # .ranking-name内のdivに星評価が入っている
                rating_div = item.locator('.ranking-name div')

                if rating_div.count() == 0:
                    continue  # 評価なしの場合スキップ

                stars_text = rating_div.text_content()

                # 星（★と☆）の総数をカウント
                star_count = stars_text.count('★') + stars_text.count('☆')

                print(f"{spot_name}: 星の総数 = {star_count}個")

                if star_count > 5:
                    print(f"  ❌ 星が5個を超えています（{star_count}個）")
                    all_valid = False
                elif star_count < 5:
                    print(f"  ⚠️  警告: 星が5個未満です（{star_count}個）")
                    all_valid = False

            browser.close()

            if all_valid:
                print("✅ 合格: 全ての観光地の星評価が5個で正しいです")
                return True
            else:
                print("❌ 不合格: 星評価の表示に問題があります。Issue Eの「どうあるべきか」を確認してください。")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue E: 人気ランキングの星評価チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_ranking_star_count()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
