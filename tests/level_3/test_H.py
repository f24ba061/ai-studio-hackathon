#!/usr/bin/env python3
"""
Level 3 - Issue H のテストスクリプト
問題: 観光地検索でGLOB演算子を使用しているため大文字小文字が区別される（検索が機能しない）
期待: LIKE演算子を使用して大文字小文字を区別しない検索を実現すること
"""

import sys
from playwright.sync_api import sync_playwright


def test_case_insensitive_search():
    """
    spots.htmlで大文字小文字を区別しない検索ができるかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # spots.htmlにアクセス
            print("観光地一覧ページにアクセスしています...")
            page.goto('http://localhost:3001/spots.html', wait_until='networkidle')

            # 検索フォームが存在するか確認
            search_input = page.locator('input[type="text"]#searchInput, input[type="search"], input[placeholder*="検索"]')
            if search_input.count() == 0:
                print("❌ エラー: 検索フォームが見つかりませんでした")
                browser.close()
                return False

            print("✅ 検索フォームを見つけました")

            # 「草津」で検索して1件以上ヒットすればOK
            print("\n=== 「草津」で検索 ===")
            search_input.fill('草津')
            search_input.press('Enter')  # Enterキーで検索を実行
            page.wait_for_timeout(2000)  # 検索結果の更新を待つ

            # 表示されているspot-itemを数える
            result_count = page.evaluate('''() => {
                const items = document.querySelectorAll('.spot-item');
                return Array.from(items).filter(item => {
                    const style = window.getComputedStyle(item);
                    return style.display !== 'none';
                }).length;
            }''')
            print(f"  検索結果: {result_count}件")

            browser.close()

            # 1件以上ヒットすれば合格
            if result_count > 0:
                print("\n✅ 合格: 検索が正しく機能しています")
                print(f"   「草津」で{result_count}件の結果が得られました")
                print("   LIKE演算子を使用した検索が動作しています")
                return True
            else:
                print("\n❌ 不合格: 検索結果が0件です")
                print("   GLOB演算子ではなくLIKE演算子を使用して検索を実装してください")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue H: 大文字小文字を区別しない検索チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_case_insensitive_search()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("大文字小文字を区別しない検索が正しく実装されています。")
        print("LIKE演算子を使用した検索が動作しています。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("検索で大文字小文字が区別されています。")
        print("GLOB演算子ではなくLIKE演算子を使用して大文字小文字を区別しない検索を実装してください。")
        print("Issue Hの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
