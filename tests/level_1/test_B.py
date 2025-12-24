#!/usr/bin/env python3
"""
Level 1 - Issue B のテストスクリプト
問題: 「リアルなユーザーレビユー」という誤字
期待: 「リアルなユーザーレビュー」と表示されること
"""

import sys
from pathlib import Path


def test_review_text():
    """
    promotion.html内の「リアルなユーザーレビュー」テキストが正しいかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    promotion_html = project_root / "frontend" / "promotion.html"

    if not promotion_html.exists():
        print(f"❌ エラー: {promotion_html} が見つかりません")
        return False

    with open(promotion_html, 'r', encoding='utf-8') as f:
        content = f.read()

    # 正しいテキスト
    correct_text = "リアルなユーザーレビュー"
    # 間違ったテキスト
    wrong_text = "リアルなユーザーレビユー"

    if correct_text in content:
        print(f"✅ 合格: 「{correct_text}」が正しく表示されています")
        return True
    elif wrong_text in content:
        print(f"❌ 不合格: テキストに誤字があります。Issue Bの「どうあるべきか」を確認してください。")
        return False
    else:
        print(f"❌ エラー: レビュー関連のテキストが見つかりません")
        return False


def main():
    print("=" * 60)
    print("Level 1 - Issue B: レビューテキストの誤字チェック")
    print("=" * 60)

    result = test_review_text()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
