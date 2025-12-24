#!/usr/bin/env python3
"""
Level 4 - Issue D のテストスクリプト
問題: イベント検索でSQLインジェクション脆弱性（文字列連結でクエリを構築）
期待: プレースホルダーを使用したパラメータ化クエリに修正すること
"""

import sys
import re
from pathlib import Path


def check_sql_injection_protection():
    """
    event_repository.pyのfind_by_keywordメソッドでSQLインジェクションから保護されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    event_repo = project_root / "app" / "repositories" / "event_repository.py"

    if not event_repo.exists():
        print(f"❌ エラー: {event_repo} が見つかりません")
        return False

    with open(event_repo, 'r', encoding='utf-8') as f:
        content = f.read()

    print("SQLインジェクション脆弱性のチェックを開始します\n")

    # コメントを除外したコードを取得
    lines = content.split('\n')
    active_code = []
    in_find_by_keyword = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        # find_by_keywordメソッドの範囲を特定
        if 'def find_by_keyword' in line:
            in_find_by_keyword = True

        if in_find_by_keyword:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def find_by_keyword' not in line:
                in_find_by_keyword = False

    method_code_str = '\n'.join(method_code)

    # 脆弱なパターン: f-stringやformat、%を使った文字列連結
    vulnerable_f_string = bool(re.search(r"f['\"].*LIKE.*\{keyword\}", method_code_str, re.DOTALL))
    vulnerable_format = bool(re.search(r"\.format\(.*keyword.*\)", method_code_str))
    vulnerable_percent = bool(re.search(r"%.*keyword.*%", method_code_str))

    # 安全なパターン: プレースホルダー（?）とパラメータの使用
    # パターン1: LIKE ? または LIKE '%' || ? || '%'
    has_placeholder = bool(re.search(r"LIKE\s+['\"]?%?\?%?['\"]?", method_code_str))
    has_concat_placeholder = bool(re.search(r"LIKE\s+['\"]%['\"]?\s*\|\|\s*\?\s*\|\|\s*['\"]%['\"]?", method_code_str))
    has_parameter = bool(re.search(r'execute\s*\([^,]+,\s*[\(\[]', method_code_str))

    print("チェック結果:")
    print(f"  脆弱なf-string: {'❌ 検出' if vulnerable_f_string else '✅ 未検出'}")
    print(f"  脆弱なformat(): {'❌ 検出' if vulnerable_format else '✅ 未検出'}")
    print(f"  プレースホルダーの使用: {'✅ あり' if has_placeholder or has_concat_placeholder else '❌ なし'}")
    print(f"  パラメータ化クエリ: {'✅ あり' if has_parameter else '❌ なし'}")
    print()

    # 脆弱なパターンがなく、安全なパターンが使われていればOK
    if not (vulnerable_f_string or vulnerable_format or vulnerable_percent):
        if has_placeholder or has_concat_placeholder or has_parameter:
            print("✅ 合格: SQLインジェクション脆弱性が修正されています")
            return True
        else:
            print("⚠️  脆弱なパターンは検出されませんでしたが、安全なパラメータ化も確認できません")
            return False
    else:
        print("❌ 不合格: SQLインジェクション脆弱性が残っています。Issue Dの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 4 - Issue D: イベント検索のSQLインジェクション脆弱性チェック")
    print("=" * 60)

    result = check_sql_injection_protection()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
