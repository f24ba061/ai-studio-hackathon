#!/usr/bin/env python3
"""
Level 5 - Issue A のテストスクリプト
問題: レビュー投稿処理にトランザクション管理の不備がある
期待: 画像保存失敗時にレビューをロールバックする処理が実装されること
"""

import sys
import re
from pathlib import Path


def check_transaction_handling():
    """
    review_service.pyのcreate_review_with_photoメソッドで
    トランザクション処理が実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    review_service = project_root / "app" / "services" / "review_service.py"

    if not review_service.exists():
        print(f"❌ エラー: {review_service} が見つかりません")
        return False

    with open(review_service, 'r', encoding='utf-8') as f:
        content = f.read()

    print("トランザクション処理の実装確認を開始します\n")

    # create_review_with_photoメソッドの範囲を特定
    lines = content.split('\n')
    in_method = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        if 'def create_review_with_photo' in line:
            in_method = True

        if in_method:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def create_review_with_photo' not in line:
                in_method = False

    method_code_str = '\n'.join(method_code)

    # トランザクション処理のパターンをチェック
    # パターン1: except句内でレビューを削除
    has_delete_in_except = bool(re.search(r'except.*:(?:[^:]*\n)*?.*self\.review_repo\.delete\s*\(\s*review_id\s*\)', method_code_str, re.MULTILINE))

    # パターン2: 画像保存結果をチェックしてエラー時にレビュー削除
    has_result_check_and_delete = bool(re.search(r'if\s+not\s+.*photo_filename.*:.*delete\s*\(\s*review_id\s*\)', method_code_str, re.DOTALL))

    # パターン3: 画像保存失敗時にエラーを返す（successがfalse）
    has_error_return = bool(re.search(r"except.*:(?:[^:]*\n)*?.*return.*'success':\s*False", method_code_str, re.MULTILINE))

    # パターン4: レビューを削除する処理（どこかに存在）
    has_delete_review = bool(re.search(r'delete\s*\(\s*review_id\s*\)', method_code_str))

    print("チェック結果:")
    print(f"  except句内でレビュー削除: {'✅ あり' if has_delete_in_except else '❌ なし'}")
    print(f"  保存結果チェック＋削除: {'✅ あり' if has_result_check_and_delete else '❌ なし'}")
    print(f"  except句内でエラー返却: {'✅ あり' if has_error_return else '❌ なし'}")
    print(f"  レビュー削除処理の存在: {'✅ あり' if has_delete_review else '❌ なし'}")
    print()

    # いずれかのトランザクション処理パターンが実装されていればOK
    if has_delete_in_except or has_result_check_and_delete or (has_error_return and has_delete_review):
        print("✅ 合格: トランザクション処理が実装されています")
        return True
    else:
        print("❌ 不合格: トランザクション処理が実装されていません。Issue Aの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 5 - Issue A: トランザクション管理チェック")
    print("=" * 60)

    result = check_transaction_handling()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
