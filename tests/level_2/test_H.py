#!/usr/bin/env python3
"""
Level 2 - Issue H のテストスクリプト
問題: 統計ページの棒グラフで、データの幅が正しく表示されていない（1件でも30%の幅）
期待: 棒グラフの幅は、最大値を基準に相対的に計算されること
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_bar_chart_width():
    """
    stats.htmlの棒グラフの幅が正しく計算されているかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # stats.htmlにアクセス
            page.goto('http://localhost:3001/stats.html', wait_until='networkidle')

            # 地域別観光地数のグラフアイテムを取得
            chart_items = page.locator('#areaChart .bar-chart-item')

            if chart_items.count() == 0:
                print("❌ エラー: グラフアイテムが見つかりません")
                browser.close()
                return False

            print(f"グラフアイテムを {chart_items.count()} 個見つけました\n")

            # 各アイテムの値と幅を取得
            items_data = []
            max_value = 0

            for i in range(chart_items.count()):
                item = chart_items.nth(i)
                label = item.locator('.bar-chart-label').text_content().strip()
                value_text = item.locator('.bar-chart-value').text_content().strip()
                value = int(value_text)

                # バーの幅を取得（style属性から）
                bar = item.locator('.bar-chart-bar')
                style = bar.get_attribute('style')

                # width: XX% を抽出
                import re
                width_match = re.search(r'width:\s*(\d+(?:\.\d+)?)%', style)
                width = float(width_match.group(1)) if width_match else 0

                items_data.append({
                    'label': label,
                    'value': value,
                    'width': width
                })

                if value > max_value:
                    max_value = value

            print(f"最大値: {max_value}\n")

            all_valid = True

            # 各アイテムの幅が正しいかチェック
            for data in items_data:
                expected_width = (data['value'] / max_value) * 100 if max_value > 0 else 0

                print(f"{data['label']}: {data['value']}件")
                print(f"  実際の幅: {data['width']}%")
                print(f"  期待される幅: {expected_width:.1f}%")

                # 許容誤差を1%とする
                if abs(data['width'] - expected_width) <= 1:
                    print(f"  ✅ 正しい幅です")
                else:
                    print(f"  ❌ 幅が正しくありません")
                    all_valid = False

                print()

            browser.close()

            if all_valid:
                print("✅ 合格: 棒グラフの幅が正しく計算されています")
                return True
            else:
                print("❌ 不合格: 棒グラフの幅計算に問題があります。Issue Hの「どうあるべきか」を確認してください。")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue H: 棒グラフの幅計算チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_bar_chart_width()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
