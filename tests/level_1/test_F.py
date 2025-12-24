#!/usr/bin/env python3
"""
Level 1 - Issue F のテストスクリプト
問題: promotion.htmlのメインタイトルのフォントサイズが小さすぎる
期待: .hero h1 の font-size が 2.5rem 以上であること
"""

import re
import sys
from pathlib import Path


def test_hero_title_font_size():
    """
    promotion.html内の.hero h1のfont-sizeが適切なサイズになっているかをチェック
    """
    # promotion.htmlのパスを取得
    project_root = Path(__file__).parent.parent.parent
    promotion_html = project_root / "frontend" / "promotion.html"

    if not promotion_html.exists():
        print(f"❌ エラー: {promotion_html} が見つかりません")
        return False

    # HTMLファイルを読み込み
    with open(promotion_html, 'r', encoding='utf-8') as f:
        content = f.read()

    # .hero h1 のスタイルを探す
    # パターン: .hero h1 { ... font-size: 値; ... }
    pattern = r'\.hero\s+h1\s*\{[^}]*font-size:\s*([0-9.]+)(rem|px|em)[^}]*\}'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("❌ エラー: .hero h1 の font-size が見つかりません")
        return False

    size_value = float(match.group(1))
    size_unit = match.group(2)

    print(f"検出されたfont-size: {size_value}{size_unit}")

    # サイズのチェック
    # remの場合: 2.5以上
    # pxの場合: 40px以上（1rem ≈ 16px として計算）
    if size_unit == 'rem':
        if size_value >= 2.5:
            print(f"✅ 合格: font-size が {size_value}rem で適切です")
            return True
        else:
            print(f"❌ 不合格: メインタイトルのフォントサイズが小さすぎます。Issue Fの「どうあるべきか」を確認してください。")
            return False
    elif size_unit == 'px':
        if size_value >= 40:
            print(f"✅ 合格: font-size が {size_value}px で適切です")
            return True
        else:
            print(f"❌ 不合格: メインタイトルのフォントサイズが小さすぎます。Issue Fの「どうあるべきか」を確認してください。")
            return False
    elif size_unit == 'em':
        if size_value >= 2.5:
            print(f"✅ 合格: font-size が {size_value}em で適切です")
            return True
        else:
            print(f"❌ 不合格: メインタイトルのフォントサイズが小さすぎます。Issue Fの「どうあるべきか」を確認してください。")
            return False
    else:
        print(f"❌ エラー: 想定外の単位 '{size_unit}' が使用されています")
        return False


def main():
    """
    テストを実行してメイン関数
    """
    print("=" * 60)
    print("Level 1 - Issue F: メインタイトルのフォントサイズチェック")
    print("=" * 60)

    result = test_hero_title_font_size()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
