#!/usr/bin/env python3
"""
Level 1 - Issue E のテストスクリプト
問題: 「群馬件観光ポータル」という誤字
期待: 「群馬県観光ポータル」と表示されること
"""

import sys
from pathlib import Path


def test_gunma_prefecture_text():
    """
    promotion.html内のフッター著作権表示の「群馬県観光ポータル」テキストが正しいかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    promotion_html = project_root / "frontend" / "promotion.html"

    if not promotion_html.exists():
        print(f"❌ エラー: {promotion_html} が見つかりません")
        return False

    with open(promotion_html, 'r', encoding='utf-8') as f:
        content = f.read()

    # フッター部分を抽出
    import re
    footer_match = re.search(r'<footer>(.*?)</footer>', content, re.DOTALL)

    if not footer_match:
        print(f"❌ エラー: フッターが見つかりません")
        return False

    footer_content = footer_match.group(1)

    # 正しいテキスト
    correct_text = "群馬県観光ポータル"
    # 間違ったテキスト
    wrong_text = "群馬件観光ポータル"

    if wrong_text in footer_content:
        print(f"❌ 不合格: テキストに誤字があります。Issue Eの「どうあるべきか」を確認してください。")
        return False
    elif correct_text in footer_content:
        print(f"✅ 合格: 「{correct_text}」が正しく表示されています")
        return True
    else:
        print(f"❌ エラー: フッター内に群馬県関連のテキストが見つかりません")
        return False


def main():
    print("=" * 60)
    print("Level 1 - Issue E: 群馬県テキストの誤字チェック")
    print("=" * 60)

    result = test_gunma_prefecture_text()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
