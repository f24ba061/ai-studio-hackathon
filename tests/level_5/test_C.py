#!/usr/bin/env python3
"""
Level 5 - Issue C のテストスクリプト
問題: データベース接続のリソースリークが発生している（接続を閉じていない）
期待: finally句でデータベース接続を必ず閉じる処理が実装されること
"""

import sys
import re
from pathlib import Path


def check_resource_cleanup():
    """
    spot_repository.pyのupdate_ratingメソッドで
    データベース接続のクリーンアップが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    spot_repo = project_root / "app" / "repositories" / "spot_repository.py"

    if not spot_repo.exists():
        print(f"❌ エラー: {spot_repo} が見つかりません")
        return False

    with open(spot_repo, 'r', encoding='utf-8') as f:
        content = f.read()

    print("リソースクリーンアップの実装確認を開始します\n")

    # update_ratingメソッドの範囲を特定
    lines = content.split('\n')
    in_method = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        if 'def update_rating' in line:
            in_method = True

        if in_method:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def update_rating' not in line:
                in_method = False

    method_code_str = '\n'.join(method_code)

    # リソースクリーンアップのパターン
    # パターン1: finally句の存在
    has_finally = bool(re.search(r'\bfinally\s*:', method_code_str))

    # パターン2: finally句内でclose_db()を呼んでいる
    has_close_db_in_finally = bool(re.search(r'finally:.*close_db', method_code_str, re.DOTALL))

    # パターン3: with文の使用（コンテキストマネージャー）
    has_with_statement = bool(re.search(r'with\s+get_db\s*\(\s*\)', method_code_str))

    # パターン4: close_db()の呼び出し（finally以外でも可）
    has_close_db = bool(re.search(r'close_db\s*\(\s*conn\s*\)', method_code_str))

    print("チェック結果:")
    print(f"  finally句の使用: {'✅ あり' if has_finally else '❌ なし'}")
    print(f"  finally句内でclose_db()呼び出し: {'✅ あり' if has_close_db_in_finally else '❌ なし'}")
    print(f"  with文の使用: {'✅ あり' if has_with_statement else '❌ なし'}")
    print(f"  close_db()の呼び出し: {'✅ あり' if has_close_db else '❌ なし'}")
    print()

    # いずれかのリソースクリーンアップ方法が実装されていればOK
    if has_close_db_in_finally or has_with_statement or (has_finally and has_close_db):
        print("✅ 合格: リソースクリーンアップが実装されています")
        return True
    else:
        print("❌ 不合格: リソースクリーンアップが実装されていません。Issue Cの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 5 - Issue C: データベース接続のリソースリークチェック")
    print("=" * 60)

    result = check_resource_cleanup()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
