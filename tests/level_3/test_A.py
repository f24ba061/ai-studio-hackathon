#!/usr/bin/env python3
"""
Level 3 - Issue A のテストスクリプト
問題: YouTube動画が埋め込まれていない（静的な画像プレースホルダーのみ）
期待: 3つの観光地（草津温泉、富岡製糸場、尾瀬国立公園）にYouTube動画が埋め込まれていること
"""

import sys
from playwright.sync_api import sync_playwright


def test_youtube_embeds():
    """
    index.htmlに3つのYouTube動画が埋め込まれているかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # index.htmlにアクセス
            page.goto('http://localhost:3001/index.html', wait_until='networkidle')

            print("YouTube動画埋め込み確認を開始します\n")

            # 期待される動画ID
            expected_videos = {
                'GrEEoEmmrKs': '草津温泉',
                'OFg0mXRNDpI': '富岡製糸場',
                'o7zDfKZrlJ8': '尾瀬国立公園'
            }

            print("チェック結果:")
            results = {}

            for video_id, name in expected_videos.items():
                # YouTube埋め込みiframeを探す（video_idを含むsrc属性を持つiframe）
                iframe = page.locator(f'iframe[src*="{video_id}"]')

                if iframe.count() > 0:
                    # src属性を取得して確認
                    src = iframe.get_attribute('src')
                    # YouTubeの埋め込みURLかチェック（youtube.com/embedまたはyoutube-nocookie.com/embed）
                    if 'youtube.com/embed' in src or 'youtube-nocookie.com/embed' in src:
                        print(f"  {name}: ✅ 埋め込みあり (src={src})")
                        results[name] = True
                    else:
                        print(f"  {name}: ❌ iframeはあるが、YouTube埋め込み形式ではありません")
                        results[name] = False
                else:
                    print(f"  {name}: ❌ 埋め込みなし")
                    results[name] = False

            print()
            browser.close()

            # すべての動画が埋め込まれていればOK
            all_embedded = all(results.values())

            if all_embedded:
                print("✅ 合格: すべての観光地にYouTube動画が埋め込まれています")
                return True
            else:
                print("❌ 不合格: YouTube動画の埋め込みが不足しています")
                print("   Issue Aの「どうあるべきか」を確認してください。")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue A: YouTube動画埋め込みチェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)
    print()

    result = test_youtube_embeds()

    print()
    print("=" * 60)
    if result:
        print("✅ テスト合格")
        print()
        print("すべての観光地にYouTube動画が正しく埋め込まれています。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("YouTube動画の埋め込みに問題があります。")
        print("<iframe> タグを使用し、src属性に https://www.youtube.com/embed/VIDEO_ID を指定してください。")
        print("Issue Aの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
