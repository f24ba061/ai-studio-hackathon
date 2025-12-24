#!/usr/bin/env python3
"""
Level 4 - Issue C のテストスクリプト
問題: レビュー削除時の権限チェックがコメントアウトされている（他人のレビューも削除可能）
期待: user_idをチェックして、自分のレビューのみ削除可能にすること
"""

import sys
import re
from pathlib import Path


def check_authorization():
    """
    review_service.pyのdelete_reviewメソッドで権限チェックが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    review_service = project_root / "app" / "services" / "review_service.py"

    if not review_service.exists():
        print(f"❌ エラー: {review_service} が見つかりません")
        return False

    with open(review_service, 'r', encoding='utf-8') as f:
        content = f.read()

    print("権限チェックの実装確認を開始します\n")

    # コメントを除外したコードを取得
    lines = content.split('\n')
    active_code = []
    in_multiline_comment = False
    in_delete_review = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        # delete_reviewメソッドの範囲を特定
        if 'def delete_review' in line:
            in_delete_review = True

        if in_delete_review:
            # コメント行はスキップ（ただし行コメントのみ）
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def delete_review' not in line:
                in_delete_review = False

    method_code_str = '\n'.join(method_code)

    # 権限チェックのパターン
    # パターン1: review['user_id'] != int(user_id) または review['user_id'] != user_id
    has_user_id_check = bool(re.search(r"review\[['\"]user_id['\"]\]\s*!=\s*.*user_id", method_code_str))
    has_permission_error = bool(re.search(r'他のユーザー.*削除', method_code_str))
    has_int_conversion = bool(re.search(r'int\s*\(\s*user_id\s*\)', method_code_str))

    print("チェック結果:")
    print(f"  user_idの比較チェック: {'✅ あり' if has_user_id_check else '❌ なし'}")
    print(f"  権限エラーメッセージ: {'✅ あり' if has_permission_error else '❌ なし'}")
    print(f"  型変換処理: {'✅ あり' if has_int_conversion else '❌ なし'}")
    print()

    if has_user_id_check and has_permission_error:
        print("✅ 合格: レビュー削除の権限チェックが実装されています")
        return True
    else:
        print("❌ 不合格: レビュー削除の権限チェックが実装されていません。Issue Cの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 4 - Issue C: レビュー削除の権限チェック")
    print("=" * 60)

    result = check_authorization()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
