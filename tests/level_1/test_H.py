#!/usr/bin/env python3
"""
Level 1 - Issue H のテストスクリプト
問題: 特徴カードの閉じタグ（</div>）が不足
期待: feature-cardクラスのdivが正しく閉じられていること
"""

import re
import sys
from pathlib import Path


def test_feature_card_closing_tag():
    """
    promotion.html内の最初のfeature-card divが正しく閉じられているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    promotion_html = project_root / "frontend" / "promotion.html"

    if not promotion_html.exists():
        print(f"❌ エラー: {promotion_html} が見つかりません")
        return False

    with open(promotion_html, 'r', encoding='utf-8') as f:
        content = f.read()

    # 最初のfeature-cardブロックを抽出（豊富な観光地情報）
    pattern = r'<div class="feature-card">\s*<div class="feature-icon">🗾</div>\s*<h3>豊富な観光地情報</h3>\s*<p>.*?</p>\s*(</div>)?'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("❌ エラー: feature-card（🗾）のブロックが見つかりません")
        return False

    closing_tag = match.group(1)

    if closing_tag:
        print(f"✅ 合格: feature-card の閉じタグ </div> が正しく存在します")
        return True
    else:
        print(f"❌ 不合格: HTMLの構造に問題があります。Issue Hの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 1 - Issue H: feature-cardの閉じタグチェック")
    print("=" * 60)

    result = test_feature_card_closing_tag()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
