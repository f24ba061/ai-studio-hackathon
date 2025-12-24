#!/usr/bin/env python3
"""
Level 5 - Issue F のテストスクリプト
問題: 統計ページにキャッシュ機構がない（毎回全データを再計算）
期待: キャッシュ機構を実装し、一定時間データを保持すること
"""

import sys
import re
from pathlib import Path


def check_cache_implementation():
    """
    stats_service.pyでキャッシュ機構が実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    stats_service = project_root / "app" / "services" / "stats_service.py"

    if not stats_service.exists():
        print(f"❌ エラー: {stats_service} が見つかりません")
        return False

    with open(stats_service, 'r', encoding='utf-8') as f:
        content = f.read()

    print("キャッシュ機構の実装確認を開始します\n")

    # キャッシュ実装のパターン
    # パターン1: flask-cachingの使用
    has_flask_caching_import = bool(re.search(r'from\s+flask_caching\s+import\s+Cache|import\s+flask_caching', content))
    has_cache_decorator = bool(re.search(r'@cache\.cached|@cached', content))

    # パターン2: 簡易的なメモリキャッシュ
    has_cache_dict = bool(re.search(r'self\.cache\s*=\s*\{|cache\s*=\s*\{', content))
    has_cache_timeout = bool(re.search(r'cache_timeout|timeout', content))
    has_time_import = bool(re.search(r'import\s+time|from\s+time\s+import', content))
    has_time_check = bool(re.search(r'time\s*\(\s*\)|time\.time', content))

    # パターン3: キャッシュのキーチェック
    has_cache_key_check = bool(re.search(r'if.*in\s+.*cache|cache\.get', content))

    # パターン4: キャッシュへの保存
    has_cache_set = bool(re.search(r'cache\[.*\]\s*=|cache\.set', content))

    # パターン5: Redis等の外部キャッシュ
    has_redis = bool(re.search(r'import\s+redis|from\s+redis', content))

    print("チェック結果:")
    print(f"  flask-cachingのインポート: {'✅ あり' if has_flask_caching_import else '❌ なし'}")
    print(f"  @cachedデコレータの使用: {'✅ あり' if has_cache_decorator else '❌ なし'}")
    print(f"  キャッシュ辞書の定義: {'✅ あり' if has_cache_dict else '❌ なし'}")
    print(f"  タイムアウト設定: {'✅ あり' if has_cache_timeout else '❌ なし'}")
    print(f"  timeモジュールのインポート: {'✅ あり' if has_time_import else '❌ なし'}")
    print(f"  時刻チェック: {'✅ あり' if has_time_check else '❌ なし'}")
    print(f"  キャッシュキーのチェック: {'✅ あり' if has_cache_key_check else '❌ なし'}")
    print(f"  キャッシュへの保存: {'✅ あり' if has_cache_set else '❌ なし'}")
    print(f"  Redis等の使用: {'✅ あり' if has_redis else '❌ なし'}")
    print()

    # いずれかのキャッシュ実装が確認できればOK
    flask_caching_ok = has_flask_caching_import and has_cache_decorator
    memory_cache_ok = has_cache_dict and has_cache_key_check and has_cache_set
    time_based_cache_ok = has_cache_dict and has_time_import and has_time_check
    redis_ok = has_redis

    if flask_caching_ok or memory_cache_ok or time_based_cache_ok or redis_ok:
        print("✅ 合格: キャッシュ機構が実装されています")
        return True
    else:
        print("❌ 不合格: キャッシュ機構が実装されていません。Issue Fの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 5 - Issue F: キャッシュ機構の実装チェック")
    print("=" * 60)

    result = check_cache_implementation()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
