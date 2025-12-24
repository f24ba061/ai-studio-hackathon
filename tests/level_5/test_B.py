#!/usr/bin/env python3
"""
Level 5 - Issue B のテストスクリプト
問題: 画像アップロード機能にファイル拡張子偽装対策が不足している
期待: ファイルの実際の種別（MIMEタイプやマジックナンバー）を検証すること
"""

import sys
import re
from pathlib import Path


def check_file_validation():
    """
    file_service.pyのvalidate_imageメソッドで
    マジックナンバーチェックが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    file_service = project_root / "app" / "services" / "file_service.py"

    if not file_service.exists():
        print(f"❌ エラー: {file_service} が見つかりません")
        return False

    with open(file_service, 'r', encoding='utf-8') as f:
        content = f.read()

    print("ファイル検証の実装確認を開始します\n")

    # validate_imageメソッドの範囲を特定
    lines = content.split('\n')
    in_method = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        if 'def validate_image' in line or 'def save_review_photo' in line:
            if in_method:
                # 次のメソッドが来たら前のメソッドは終了
                in_method = False
            if 'def validate_image' in line:
                in_method = True

        if in_method:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)

    method_code_str = '\n'.join(method_code)

    # マジックナンバーチェックのパターン
    # パターン1: imghdrモジュールの使用
    has_imghdr_import = bool(re.search(r'import\s+imghdr', content))
    has_imghdr_what = bool(re.search(r'imghdr\.what', method_code_str))

    # パターン2: PILライブラリの使用
    has_pil_import = bool(re.search(r'from\s+PIL\s+import\s+Image|import\s+PIL', content))
    has_image_open = bool(re.search(r'Image\.open', method_code_str))
    has_image_verify = bool(re.search(r'\.verify\s*\(\s*\)', method_code_str))

    # パターン3: MIMEタイプのチェック
    has_content_type_check = bool(re.search(r'file\.content_type|content_type', method_code_str))

    # パターン4: マジックナンバーの直接チェック
    has_magic_number_check = bool(re.search(r'file\.read\(.*\)|\.startswith\(', method_code_str))

    # パターン5: file.read()の使用（ファイル内容の読み取り）
    has_file_read = bool(re.search(r'file\.read\s*\(', method_code_str))

    print("チェック結果:")
    print(f"  imghdrモジュールのインポート: {'✅ あり' if has_imghdr_import else '❌ なし'}")
    print(f"  imghdr.what()の使用: {'✅ あり' if has_imghdr_what else '❌ なし'}")
    print(f"  PILライブラリのインポート: {'✅ あり' if has_pil_import else '❌ なし'}")
    print(f"  Image.open()の使用: {'✅ あり' if has_image_open else '❌ なし'}")
    print(f"  Image.verify()の使用: {'✅ あり' if has_image_verify else '❌ なし'}")
    print(f"  content_typeのチェック: {'✅ あり' if has_content_type_check else '❌ なし'}")
    print(f"  ファイル内容の読み取り: {'✅ あり' if has_file_read else '❌ なし'}")
    print()

    # いずれかのファイル検証方法が実装されていればOK
    imghdr_ok = has_imghdr_import and has_imghdr_what
    pil_ok = has_pil_import and (has_image_open or has_image_verify)
    content_type_ok = has_content_type_check
    manual_check_ok = has_file_read and has_magic_number_check

    if imghdr_ok or pil_ok or content_type_ok or manual_check_ok:
        print("✅ 合格: ファイル内容の検証が実装されています")
        return True
    else:
        print("❌ 不合格: ファイル内容の検証が実装されていません。Issue Bの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 5 - Issue B: ファイル拡張子偽装対策チェック")
    print("=" * 60)

    result = check_file_validation()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
