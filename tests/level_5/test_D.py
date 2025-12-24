#!/usr/bin/env python3
"""
Level 5 - Issue D のテストスクリプト
問題: レビュー表示時にN+1クエリ問題が発生している
期待: JOINを使ってレビューとユーザー情報を一度に取得すること
"""

import sys
import re
from pathlib import Path


def check_n_plus_one_fix():
    """
    review_repository.pyのfind_by_spot_idメソッドで
    JOINが使われているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    review_repo = project_root / "app" / "repositories" / "review_repository.py"

    if not review_repo.exists():
        print(f"❌ エラー: {review_repo} が見つかりません")
        return False

    with open(review_repo, 'r', encoding='utf-8') as f:
        content = f.read()

    print("N+1クエリ問題の修正確認を開始します\n")

    # find_by_spot_idメソッドの範囲を特定
    lines = content.split('\n')
    in_method = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        if 'def find_by_spot_id' in line:
            in_method = True

        if in_method:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def find_by_spot_id' not in line:
                in_method = False

    method_code_str = '\n'.join(method_code)

    # JOINを使ったクエリのパターン
    # パターン1: JOIN users
    has_join_users = bool(re.search(r'JOIN\s+users', method_code_str, re.IGNORECASE))

    # パターン2: LEFT JOIN users
    has_left_join = bool(re.search(r'LEFT\s+JOIN\s+users', method_code_str, re.IGNORECASE))

    # パターン3: INNER JOIN users
    has_inner_join = bool(re.search(r'INNER\s+JOIN\s+users', method_code_str, re.IGNORECASE))

    # パターン4: user_nameをSELECT句で取得
    has_user_name_select = bool(re.search(r'u\.name.*as\s+user_name|user_name', method_code_str, re.IGNORECASE))

    # パターン5: ON r.user_id = u.user_id のような結合条件
    has_join_condition = bool(re.search(r'ON\s+.*user_id.*=.*user_id', method_code_str, re.IGNORECASE))

    print("チェック結果:")
    print(f"  JOIN users の使用: {'✅ あり' if has_join_users else '❌ なし'}")
    print(f"  LEFT JOIN の使用: {'✅ あり' if has_left_join else '❌ なし'}")
    print(f"  INNER JOIN の使用: {'✅ あり' if has_inner_join else '❌ なし'}")
    print(f"  user_name の取得: {'✅ あり' if has_user_name_select else '❌ なし'}")
    print(f"  JOIN条件の指定: {'✅ あり' if has_join_condition else '❌ なし'}")
    print()

    # JOINが使われていればOK
    if (has_join_users or has_left_join or has_inner_join) and has_join_condition:
        print("✅ 合格: JOINを使ったクエリが実装されています")
        return True
    else:
        print("❌ 不合格: JOINを使ったクエリが実装されていません。Issue Dの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 5 - Issue D: N+1クエリ問題の修正チェック")
    print("=" * 60)

    result = check_n_plus_one_fix()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
