#!/usr/bin/env python3
"""
Level 5 - Issue G のテストスクリプト
問題: 月フィルターと地域フィルターを同時に使用できない（片方を選ぶともう片方がリセットされる）
期待: 月フィルターと地域フィルターを組み合わせて使用できること
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_combined_filters():
    """
    月フィルターと地域フィルターを組み合わせて使用できるかをチェック（Playwright）
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # events.htmlにアクセス
            page.goto('http://localhost:3001/events.html', wait_until='networkidle')
            page.wait_for_timeout(1000)

            # 月フィルター「8月」を選択
            month_buttons = page.locator('#monthFilter .filter-btn')
            august_button = None
            for i in range(month_buttons.count()):
                button = month_buttons.nth(i)
                if '8月' in button.text_content():
                    august_button = button
                    break

            if not august_button:
                print("❌ エラー: 8月ボタンが見つかりません")
                browser.close()
                return False

            august_button.click()
            page.wait_for_timeout(1000)

            # 月フィルターがアクティブかチェック
            august_active_after_month = august_button.get_attribute('class')
            print(f"8月フィルター選択後のクラス: {august_active_after_month}")

            # 地域フィルター「草津」を選択
            area_buttons = page.locator('#areaFilter .filter-btn')
            kusatsu_button = None
            for i in range(area_buttons.count()):
                button = area_buttons.nth(i)
                if '草津' in button.text_content():
                    kusatsu_button = button
                    break

            if not kusatsu_button:
                print("❌ エラー: 草津ボタンが見つかりません")
                browser.close()
                return False

            kusatsu_button.click()
            page.wait_for_timeout(1000)

            # 地域フィルター選択後も月フィルターがアクティブか確認
            august_active_after_area = august_button.get_attribute('class')
            kusatsu_active = kusatsu_button.get_attribute('class')

            print(f"地域フィルター選択後の8月クラス: {august_active_after_area}")
            print(f"地域フィルター選択後の草津クラス: {kusatsu_active}")
            print()

            browser.close()

            month_still_active = 'active' in august_active_after_area if august_active_after_area else False
            area_active = 'active' in kusatsu_active if kusatsu_active else False

            if month_still_active and area_active:
                print("✅ 合格: 月フィルターと地域フィルターを組み合わせて使用できます")
                return True
            elif not month_still_active:
                print("❌ 不合格: 地域フィルターを選択すると月フィルターがリセットされます。Issue Gの「どうあるべきか」を確認してください。")
                return False
            else:
                print("⚠️  想定外の状態です")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def check_source_code():
    """
    events.jsで月フィルターと地域フィルターの組み合わせが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    events_js = project_root / "frontend" / "events.js"

    if not events_js.exists():
        print(f"❌ エラー: {events_js} が見つかりません")
        return False

    with open(events_js, 'r', encoding='utf-8') as f:
        content = f.read()

    # コメントを除外したコードを取得
    lines = content.split('\n')
    active_code = []
    in_multiline_comment = False

    for line in lines:
        stripped = line.strip()

        if '/*' in stripped:
            in_multiline_comment = True

        if '*/' in stripped:
            in_multiline_comment = False
            continue

        if in_multiline_comment or stripped.startswith('//'):
            continue

        active_code.append(line)

    active_code_str = '\n'.join(active_code)

    import re
    # filterByAreaやfilterByMonthで他のフィルターをリセットしていないか
    # バグパターン: areaButtons.forEach(btn => btn.classList.remove('active'))がfilterByMonthにある
    # バグパターン: monthButtons.forEach(btn => btn.classList.remove('active'))がfilterByAreaにある

    # 修正済みパターン: currentFilterに両方の値を保持、またはAPIに両方のパラメータを渡す
    has_combined_filter = bool(re.search(r'month.*area|area.*month', active_code_str))
    has_both_params = bool(re.search(r'getEventsByMonthAndArea', active_code_str))
    has_filter_object = bool(re.search(r'currentFilter\.(month|area)', active_code_str))

    print("\nソースコードチェック:")
    print(f"  複合フィルターロジック: {'✅ あり' if has_combined_filter else '❌ なし'}")
    print(f"  両パラメータAPI呼び出し: {'✅ あり' if has_both_params else '❌ なし'}")
    print(f"  currentFilterオブジェクト: {'✅ あり' if has_filter_object else '❌ なし'}")
    print()

    if (has_combined_filter or has_both_params) and has_filter_object:
        print("✅ 合格: フィルター組み合わせのロジックが実装されています")
        return True
    else:
        print("❌ 不合格: フィルター組み合わせが実装されていません。Issue Gの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 5 - Issue G: 月・地域フィルター組み合わせチェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    # まずPlaywrightでテスト
    result = test_combined_filters()

    # 失敗したらソースコードもチェック
    if not result:
        print("\n【追加チェック: ソースコード確認】")
        result = check_source_code()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
