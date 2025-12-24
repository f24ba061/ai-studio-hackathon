#!/usr/bin/env python3
"""
Level 1 - Issue A のテストスクリプト
問題: 「イベント上報満載」という誤字
期待: 「イベント情報満載」と表示されること
"""

import sys
from pathlib import Path


def test_event_info_text():
    """
    promotion.html内の「イベント情報満載」テキストが正しいかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    promotion_html = project_root / "frontend" / "promotion.html"

    if not promotion_html.exists():
        print(f"❌ エラー: {promotion_html} が見つかりません")
        return False

    with open(promotion_html, 'r', encoding='utf-8') as f:
        content = f.read()

    # 正しいテキスト
    correct_text = "イベント情報満載"
    # 間違ったテキスト
    wrong_text = "イベント上報満載"

    if correct_text in content:
        print(f"✅ 合格: 「{correct_text}」が正しく表示されています")
        return True
    elif wrong_text in content:
        print(f"❌ 不合格: テキストに誤字があります。Issue Aの「どうあるべきか」を確認してください。")
        return False
    else:
        print(f"❌ エラー: イベント関連のテキストが見つかりません")
        return False


def main():
    print("=" * 60)
    print("Level 1 - Issue A: イベントテキストの誤字チェック")
    print("=" * 60)

    result = test_event_info_text()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
