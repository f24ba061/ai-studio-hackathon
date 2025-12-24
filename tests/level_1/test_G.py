#!/usr/bin/env python3
"""
Level 1 - Issue G のテストスクリプト
問題: ヒーローセクションの背景グラデーションのカラーコードが不完全
期待: #667eea（完全な6桁のカラーコード）が使用されていること
"""

import re
import sys
from pathlib import Path


def test_hero_gradient_color():
    """
    promotion.html内の.heroのグラデーションカラーコードが正しいかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    promotion_html = project_root / "frontend" / "promotion.html"

    if not promotion_html.exists():
        print(f"❌ エラー: {promotion_html} が見つかりません")
        return False

    with open(promotion_html, 'r', encoding='utf-8') as f:
        content = f.read()

    # .hero のbackground: linear-gradientを探す（最初のカラーコードを取得）
    pattern = r'\.hero\s*\{[^}]*background:\s*linear-gradient\([^#]*#([0-9a-fA-F]+)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("❌ エラー: .hero の background: linear-gradient が見つかりません")
        return False

    first_color = match.group(1).lower()
    print(f"検出されたカラーコード（最初）: #{first_color}")

    # #667eea が正しいカラーコード
    if first_color == '667eea':
        print(f"✅ 合格: カラーコードが #{first_color} で正しいです")
        return True
    else:
        print(f"❌ 不合格: ヒーローセクションの背景グラデーションが正しくありません。Issue Gの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 1 - Issue G: ヒーローセクションの背景グラデーションチェック")
    print("=" * 60)

    result = test_hero_gradient_color()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
