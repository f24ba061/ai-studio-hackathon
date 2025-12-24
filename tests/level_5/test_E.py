#!/usr/bin/env python3
"""
Level 5 - Issue E のテストスクリプト
問題: 月別イベント集計のGROUP BY句に不要なevent_idが含まれている
期待: GROUP BY句にはmonthのみを指定すること
"""

import sys
import re
from pathlib import Path


def check_group_by():
    """
    stats_repository.pyのfetch_events_by_monthメソッドで
    GROUP BY句が正しく指定されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    stats_repo = project_root / "app" / "repositories" / "stats_repository.py"

    if not stats_repo.exists():
        print(f"❌ エラー: {stats_repo} が見つかりません")
        return False

    with open(stats_repo, 'r', encoding='utf-8') as f:
        content = f.read()

    print("GROUP BY句の確認を開始します\n")

    # fetch_events_by_monthメソッドの範囲を特定
    lines = content.split('\n')
    in_method = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        if 'def fetch_events_by_month' in line:
            in_method = True

        if in_method:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def fetch_events_by_month' not in line:
                in_method = False

    method_code_str = '\n'.join(method_code)

    # GROUP BY句のパターン
    # 脆弱なパターン: GROUP BY month, event_id
    has_event_id_in_group_by = bool(re.search(r'GROUP\s+BY\s+.*event_id', method_code_str, re.IGNORECASE))

    # 正しいパターン: GROUP BY month のみ
    has_month_only_group_by = bool(re.search(r'GROUP\s+BY\s+month\s*(?:ORDER|$)', method_code_str, re.IGNORECASE))

    # GROUP BY句の存在
    has_group_by = bool(re.search(r'GROUP\s+BY', method_code_str, re.IGNORECASE))

    print("チェック結果:")
    print(f"  GROUP BY句の存在: {'✅ あり' if has_group_by else '❌ なし'}")
    print(f"  GROUP BY month, event_id: {'❌ 検出（問題あり）' if has_event_id_in_group_by else '✅ 未検出'}")
    print(f"  GROUP BY month（のみ）: {'✅ 検出' if has_month_only_group_by else '❌ 未検出'}")
    print()

    # event_idがGROUP BYに含まれていなければOK
    if has_group_by and not has_event_id_in_group_by:
        print("✅ 合格: GROUP BY句が正しく指定されています")
        return True
    elif has_event_id_in_group_by:
        print("❌ 不合格: GROUP BY句にevent_idが含まれています。Issue Eの「どうあるべきか」を確認してください。")
        return False
    else:
        print("❌ 不合格: GROUP BY句が見つかりません")
        return False


def main():
    print("=" * 60)
    print("Level 5 - Issue E: GROUP BY句のチェック")
    print("=" * 60)

    result = check_group_by()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
