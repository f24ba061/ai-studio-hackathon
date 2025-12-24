#!/usr/bin/env python3
"""
Level 4 - Issue E のテストスクリプト
問題: 統計API（地域別観光地数取得）でSQLインジェクション脆弱性（area_filterを直接埋め込み）
期待: プレースホルダーを使用したパラメータ化クエリに修正すること
"""

import sys
import re
from pathlib import Path


def check_sql_injection_protection():
    """
    stats_repository.pyのfetch_spots_by_areaメソッドでSQLインジェクションから保護されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    stats_repo = project_root / "app" / "repositories" / "stats_repository.py"

    if not stats_repo.exists():
        print(f"❌ エラー: {stats_repo} が見つかりません")
        return False

    with open(stats_repo, 'r', encoding='utf-8') as f:
        content = f.read()

    print("SQLインジェクション脆弱性のチェックを開始します\n")

    # コメントを除外したコードを取得
    lines = content.split('\n')
    in_multiline_comment = False
    in_get_spots_by_area = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        # fetch_spots_by_areaメソッドの範囲を特定
        if 'def fetch_spots_by_area' in line:
            in_get_spots_by_area = True

        if in_get_spots_by_area:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def fetch_spots_by_area' not in line:
                in_get_spots_by_area = False

    method_code_str = '\n'.join(method_code)

    # 脆弱なパターン: f-stringやformat、%を使った文字列連結（area_filter）
    vulnerable_f_string = bool(re.search(r'f["\'].*\{area_filter\}', method_code_str))
    vulnerable_format = bool(re.search(r"\.format\(.*area_filter.*\)", method_code_str))

    # 安全なパターン: プレースホルダー（?）とパラメータの使用
    has_placeholder = bool(re.search(r"LIKE\s+['\"]?%?\?%?['\"]?", method_code_str))
    has_parameter_in_execute = bool(re.search(r'execute\s*\([^,]+,\s*[\(\[]', method_code_str))

    print("チェック結果:")
    print(f"  脆弱なf-string: {'❌ 検出' if vulnerable_f_string else '✅ 未検出'}")
    print(f"  脆弱なformat(): {'❌ 検出' if vulnerable_format else '✅ 未検出'}")
    print(f"  プレースホルダーの使用: {'✅ あり' if has_placeholder else '❌ なし'}")
    print(f"  パラメータ化クエリ: {'✅ あり' if has_parameter_in_execute else '❌ なし'}")
    print()

    # 脆弱なパターンがなく、安全なパターンが使われていればOK
    if not (vulnerable_f_string or vulnerable_format):
        if has_placeholder or has_parameter_in_execute:
            print("✅ 合格: SQLインジェクション脆弱性が修正されています")
            return True
        else:
            print("⚠️  脆弱なパターンは検出されませんでしたが、安全なパラメータ化も確認できません")
            return False
    else:
        print("❌ 不合格: SQLインジェクション脆弱性が残っています。Issue Eの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 4 - Issue E: 統計APIのSQLインジェクション脆弱性チェック")
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
