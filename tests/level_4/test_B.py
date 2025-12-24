#!/usr/bin/env python3
"""
Level 4 - Issue B のテストスクリプト
問題: イベント名表示でXSS脆弱性（event_nameをエスケープせずにHTMLに挿入）
期待: event_nameをエスケープしてから表示すること、またはtextContentを使用すること
"""

import sys
import re
from pathlib import Path


def check_xss_protection():
    """
    events.jsでイベント名がXSSから保護されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    events_js = project_root / "frontend" / "events.js"

    if not events_js.exists():
        print(f"❌ エラー: {events_js} が見つかりません")
        return False

    with open(events_js, 'r', encoding='utf-8') as f:
        content = f.read()

    print("XSS脆弱性のチェックを開始します\n")

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

    # パターン1: エスケープ関数を使用しているか
    has_escape_function = bool(re.search(r'function\s+escapeHtml\s*\(', active_code_str))
    uses_escape_on_event_name = bool(re.search(r'escapeHtml\s*\(\s*event\.event_name\s*\)', active_code_str))

    # パターン2: textContentを使用しているか
    uses_text_content = bool(re.search(r'\.textContent\s*=\s*event\.event_name', active_code_str))

    # パターン3: 安全なDOM操作を使用しているか（createElement + textContent）
    uses_safe_dom = bool(re.search(r'createElement.*textContent.*event_name', active_code_str, re.DOTALL))

    # 脆弱なパターン: event_nameを直接HTMLに挿入
    vulnerable_pattern = bool(re.search(r'\$\{event\.event_name\}', active_code_str))

    print("チェック結果:")
    print(f"  エスケープ関数の定義: {'✅ あり' if has_escape_function else '❌ なし'}")
    print(f"  event_nameのエスケープ: {'✅ あり' if uses_escape_on_event_name else '❌ なし'}")
    print(f"  textContentの使用: {'✅ あり' if uses_text_content else '❌ なし'}")
    print(f"  脆弱なパターン: {'❌ 検出' if vulnerable_pattern else '✅ 未検出'}")
    print()

    # いずれかの保護手段が実装されていればOK
    if (has_escape_function and uses_escape_on_event_name) or uses_text_content or uses_safe_dom:
        if not vulnerable_pattern:
            print("✅ 合格: XSS脆弱性が修正されています")
            return True
        else:
            print("⚠️  エスケープ処理は実装されていますが、脆弱なパターンも残っています")
            return False
    else:
        print("❌ 不合格: XSS脆弱性が修正されていません。Issue Bの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 4 - Issue B: イベント名表示のXSS脆弱性チェック")
    print("=" * 60)

    result = check_xss_protection()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
