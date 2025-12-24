#!/usr/bin/env python3
"""
Level 1 - Issue I のテストスクリプト
問題: spot.html へのリンクが404エラー
期待: spots.html（複数形）へのリンクが正しく設定されていること
"""

import re
import sys
from pathlib import Path


def test_spots_link():
    """
    promotion.html内の観光地ページへのリンクが正しいかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    promotion_html = project_root / "frontend" / "promotion.html"

    if not promotion_html.exists():
        print(f"❌ エラー: {promotion_html} が見つかりません")
        return False

    with open(promotion_html, 'r', encoding='utf-8') as f:
        content = f.read()

    # 「今すぐ観光地を探す」ボタンのhrefを探す
    pattern = r'<a\s+href="([^"]+)"\s+class="cta-button">今すぐ観光地を探す</a>'
    match = re.search(pattern, content)

    if not match:
        print("❌ エラー: 「今すぐ観光地を探す」ボタンが見つかりません")
        return False

    href = match.group(1)
    print(f"検出されたリンク先: {href}")

    if href == "spots.html":
        print(f"✅ 合格: リンク先が spots.html で正しいです")
        return True
    else:
        print(f"❌ 不合格: リンク先が正しくありません。Issue Iの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 1 - Issue I: 観光地ページリンクチェック")
    print("=" * 60)

    result = test_spots_link()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
