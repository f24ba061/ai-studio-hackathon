# 群馬県観光地レビューアプリ - 講師用ガイド

このドキュメントは、ハッカソン・授業の実施者向けの詳細ガイドです。

## 📋 目次

- [プロジェクト構成](#プロジェクト構成)
- [技術アーキテクチャ](#技術アーキテクチャ)
- [データベース詳細](#データベース詳細)
- [APIエンドポイント](#apiエンドポイント)
- [自動採点システム](#自動採点システム)
- [テンプレートの作成方法](#テンプレートの作成方法)
- [issueの管理](#issueの管理)
- [テストスクリプトの作成](#テストスクリプトの作成)

---

## プロジェクト構成

```
ai-studio-hackathon/
├── README.md                      # 学生用README
├── README_INSTRUCTOR.md           # このファイル（講師用）
├── SPECIFICATION.md               # API仕様書
├── docker-compose.yml             # Docker Compose設定
├── Dockerfile                     # Dockerイメージ定義
├── docker-entrypoint.sh           # Docker起動スクリプト
├── requirements.txt              # Python依存関係
├── .github/
│   └── workflows/
│       └── auto-grade.yml        # 自動採点ワークフロー
├── database/                      # データベース関連
│   ├── schema.sql                # テーブル定義（参考用）
│   ├── init_db.py                # データベース初期化
│   ├── add_tourist_spots.py      # 群馬県観光地データ追加
│   ├── add_sample_users.py       # サンプルユーザー追加
│   ├── add_sample_reviews.py     # サンプルレビュー追加
│   ├── add_sample_events.py      # サンプルイベント追加
│   └── add_photo_review.py       # 画像付きレビュー追加
├── app/                          # バックエンド（3層アーキテクチャ）
│   ├── app.py                    # メインアプリケーション
│   ├── config.py                 # 設定ファイル
│   ├── controllers/              # コントローラー層
│   │   ├── spot_controller.py    # 観光地エンドポイント
│   │   ├── review_controller.py  # レビューエンドポイント
│   │   ├── auth_controller.py    # 認証エンドポイント
│   │   ├── event_controller.py   # イベントエンドポイント
│   │   ├── stats_controller.py   # 統計エンドポイント
│   │   └── static_controller.py  # 静的ファイル配信
│   ├── services/                 # サービス層（ビジネスロジック）
│   │   ├── spot_service.py       # 観光地ビジネスロジック
│   │   ├── review_service.py     # レビュービジネスロジック
│   │   ├── auth_service.py       # 認証ビジネスロジック
│   │   ├── event_service.py      # イベントビジネスロジック
│   │   ├── file_service.py       # ファイル処理
│   │   └── stats_service.py      # 統計処理
│   └── repositories/             # リポジトリ層（データアクセス）
│       ├── database.py           # データベース接続
│       ├── spot_repository.py    # 観光地データアクセス
│       ├── review_repository.py  # レビューデータアクセス
│       ├── user_repository.py    # ユーザーデータアクセス
│       ├── event_repository.py   # イベントデータアクセス
│       └── stats_repository.py   # 統計データアクセス
├── frontend/                      # フロントエンド
│   ├── index.html                # トップページ
│   ├── spots.html                # 観光スポット一覧
│   ├── spot-detail.html          # 観光スポット詳細
│   ├── events.html               # イベント一覧
│   ├── stats.html                # 統計ページ
│   ├── promotion.html            # 宣伝ページ
│   ├── credits.html              # 画像クレジット
│   ├── styles.css                # スタイルシート
│   ├── api-client.js             # API通信クライアント
│   ├── spots.js                  # 観光スポット一覧のJavaScript
│   ├── spot-detail.js            # 観光スポット詳細のJavaScript
│   ├── events.js                 # イベント一覧のJavaScript
│   └── stats.js                  # 統計ページのJavaScript
├── issues/                        # issue定義（Markdown）
│   ├── level_1/                  # 超初級（A-J: 10問）
│   ├── level_2/                  # 初級（A-J: 10問）
│   ├── level_3/                  # 中級（A-J: 10問）
│   ├── level_4/                  # 上級（A-E: 5問）
│   └── level_5/                  # 最上級（A-G: 7問）
└── tests/                         # テストスクリプト
    ├── level_1/                  # Level 1テスト（test_A.py 〜 test_J.py）
    ├── level_2/                  # Level 2テスト（test_A.py 〜 test_J.py）
    ├── level_3/                  # Level 3テスト（test_A.py 〜 test_J.py）
    ├── level_4/                  # Level 4テスト（test_A.py 〜 test_E.py）
    └── level_5/                  # Level 5テスト（test_A.py 〜 test_G.py）
```

---

## 技術アーキテクチャ

### 3層アーキテクチャ

このアプリケーションは、保守性と拡張性を重視した3層アーキテクチャで設計されています。

```
┌─────────────────────────────────────────┐
│         Controller Layer                │  ← HTTPリクエスト/レスポンス
│  (spot_controller.py, review_controller.py, etc.) │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          Service Layer                  │  ← ビジネスロジック
│   (spot_service.py, review_service.py, etc.)   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│        Repository Layer                 │  ← データアクセス
│  (spot_repository.py, review_repository.py, etc.) │
└─────────────────────────────────────────┘
                    ↓
              SQLite Database
```

#### Controller層の役割
- HTTPリクエストの受信
- リクエストパラメータのバリデーション
- Serviceレイヤーの呼び出し
- HTTPレスポンスの返却

#### Service層の役割
- ビジネスロジックの実装
- トランザクション管理
- 複数のRepositoryの組み合わせ
- エラーハンドリング

#### Repository層の役割
- データベースへのCRUD操作
- SQLクエリの実行
- データの取得・保存

---

## データベース詳細

### スキーマ定義

⚠️ **重要**: データベースのスキーマ定義は `database/init_db.py` に記載されています。
- `database/schema.sql` はドキュメント・参考用です（実際の初期化には使用されません）
- Docker起動時やセットアップ時は `database/init_db.py` が実行されます

### テーブル構成

#### users（ユーザー）
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### tourist_spots（観光地）
```sql
CREATE TABLE tourist_spots (
    spot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    spot_name TEXT NOT NULL,
    address TEXT NOT NULL,
    description TEXT,
    avg_rating REAL DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**トリガー**: レビュー追加・削除時に `avg_rating` と `review_count` を自動更新

#### reviews（レビュー）
```sql
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    spot_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    photo_filename TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (spot_id) REFERENCES tourist_spots(spot_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
```

#### events（イベント）
```sql
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    location TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### 初期データ

- **ユーザー**: 4名（テストユーザー + サンプルユーザー3名）
- **観光地**: 21ヶ所（草津温泉、伊香保温泉、尾瀬、富岡製糸場など）
- **レビュー**: 38件（主要観光地へのサンプルレビュー）
- **イベント**: 20件（高崎だるま市、桐生八木節まつり、前橋花火大会など）

---

## APIエンドポイント

詳細は [SPECIFICATION.md](./SPECIFICATION.md) を参照してください。

### 観光地 API
- `GET /api/spots` - 観光地一覧取得
- `GET /api/spots/{spot_id}` - 観光地詳細取得
- `GET /api/spots/search?keyword={keyword}` - 観光地検索

### レビュー API
- `GET /api/reviews/{spot_id}` - レビュー一覧取得
- `POST /api/reviews` - レビュー投稿
- `DELETE /api/reviews/{review_id}` - レビュー削除

### イベント API
- `GET /api/events` - イベント一覧取得
- `GET /api/events?month={month}` - 月別イベント取得
- `GET /api/events?area={area}` - 地域別イベント取得
- `GET /api/events/search?q={keyword}` - イベント検索

### 認証 API
- `POST /api/auth` - ユーザー認証
- `POST /api/users` - ユーザー登録

### 統計 API
- `GET /api/stats/summary` - 基本統計情報取得
- `GET /api/stats/spots-by-area` - 地域別観光地数取得
- `GET /api/stats/events-by-month` - 月別イベント数取得
- `GET /api/stats/top-spots` - 人気観光地ランキング取得

---

## 自動採点システム

### 仕組み

GitHub Actionsを使用した自動採点システムを実装しています。

```
学生がPRを作成
       ↓
ラベルを付与（例: level_1/A）
       ↓
GitHub Actionsがトリガー
       ↓
Dockerでアプリケーション起動
       ↓
テストスクリプト実行
       ↓
結果をPRにコメント
```

### ワークフローファイル

`.github/workflows/auto-grade.yml` に定義されています。

**主要な設定:**
- トリガー: `pull_request` の `labeled` イベント
- 条件: ラベル名に基づいて対応するジョブを実行
- 実行環境: `ubuntu-latest`
- Python: 3.11
- Docker: docker compose を使用

**テストの種類:**

1. **ソースコードチェック** (静的解析)
   - HTMLのスペルミス
   - CSSのプロパティエラー
   - JavaScriptの構文エラー
   - SQLインジェクション脆弱性
   - XSS脆弱性

2. **Playwrightテスト** (動的チェック)
   - ブラウザ自動操作
   - UI/UXの確認
   - JavaScriptの動作確認
   - 12個のテスト（Level 2: A-J, Level 3: E, J）

### ラベル一覧

| ラベル | テスト内容 |
|--------|------------|
| `level_1/A` 〜 `level_1/J` | HTML/CSS基本チェック |
| `level_2/A` 〜 `level_2/J` | JavaScript基本チェック（Playwright使用） |
| `level_3/A` 〜 `level_3/J` | バリデーション・エラーハンドリング |
| `level_4/A` 〜 `level_4/E` | セキュリティ脆弱性（XSS、SQLインジェクション等） |
| `level_5/A` 〜 `level_5/G` | パフォーマンス・データ整合性 |

### テスト実行の流れ

#### ソースコードチェックのみの場合
```yaml
steps:
  - name: Checkout code
  - name: Setup Python
  - name: Run Test
  - name: Comment result
  - name: Check test result
```

#### Playwrightテストの場合
```yaml
steps:
  - name: Checkout code
  - name: Setup Python
  - name: Install Playwright
  - name: Start application with Docker  # アプリ起動
  - name: Run Test
  - name: Stop application               # アプリ停止
  - name: Comment result
  - name: Check test result
```

---

## テンプレートの作成方法

### 1. GitHubでテンプレート化

1. GitHubリポジトリページに移動
2. **Settings** タブをクリック
3. **Template repository** にチェックを入れる

これで完了！学生は「Use this template」ボタンから自分のリポジトリを作成できます。

### 2. テンプレートに含まれるもの・含まれないもの

**✅ 含まれるもの:**
- ソースコード
- README.md（学生用）
- README_INSTRUCTOR.md（講師用）
- GitHub Actions ワークフロー
- issue定義（`issues/`ディレクトリ）
- テストスクリプト（`tests/`ディレクトリ）
- Dockerfile, docker-compose.yml

**❌ 含まれないもの:**
- データベースファイル（`.gitignore`で除外）
- コミット履歴
- ブランチ（デフォルトブランチのみ）
- Pull Requests
- Issues（GitHub issue機能）

### 3. テンプレート使用時の注意点

- 学生がテンプレートから作成すると、コミット履歴はリセットされます
- 初回Docker起動時にデータベースが自動作成されます
- GitHub Actionsは自動的に有効化されます

---

## issueの管理

### issue定義ファイルの構成

各issueは `issues/level_X/Y.md` に定義されています。

**推奨フォーマット:**

```markdown
# Level X - Issue Y: [タイトル]

## 問題の説明
[バグの内容を簡潔に説明]

## 再現手順
1. [手順1]
2. [手順2]
3. [期待される動作と実際の動作]

## どうあるべきか
[正しい実装の説明]

## ヒント
- [ヒント1]
- [ヒント2]

## 関連ファイル
- `path/to/file.py`
- `path/to/file.js`
```

### 新しいissueの追加方法

1. **issue定義ファイルを作成**
   ```bash
   # 例: Level 1 - Issue K を追加
   touch issues/level_1/K.md
   ```

2. **テストスクリプトを作成**
   ```bash
   touch tests/level_1/test_K.py
   ```

3. **ワークフローに追加**
   `.github/workflows/auto-grade.yml` に新しいジョブを追加

4. **README.mdの問題数を更新**

---

## テストスクリプトの作成

### テストスクリプトの基本構造

#### ソースコードチェックの例

```python
#!/usr/bin/env python3
"""
Level X - Issue Y のテストスクリプト
問題: [問題の説明]
期待: [正しい実装]
"""

import sys
import re
from pathlib import Path

def check_fix():
    """修正内容をチェック"""
    project_root = Path(__file__).parent.parent.parent
    target_file = project_root / "path" / "to" / "file.py"

    if not target_file.exists():
        print(f"❌ エラー: {target_file} が見つかりません")
        return False

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # チェックロジック
    if "expected_pattern" in content:
        print("✅ 合格: 修正が確認されました")
        return True
    else:
        print("❌ 不合格: 修正が確認できません")
        return False

def main():
    print("=" * 60)
    print("Level X - Issue Y: [タイトル]")
    print("=" * 60)

    result = check_fix()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### Playwrightテストの例

```python
#!/usr/bin/env python3
"""
Level X - Issue Y のテストスクリプト
問題: [問題の説明]
期待: [正しい実装]
"""

import sys
from playwright.sync_api import sync_playwright

def test_with_playwright():
    """Playwrightでブラウザテスト"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # ページにアクセス
            page.goto('http://localhost:3001/page.html', wait_until='networkidle')

            # 要素をチェック
            element = page.locator('#element-id')

            if element.is_visible():
                print("✅ 合格: 要素が正しく表示されています")
                browser.close()
                return True
            else:
                print("❌ 不合格: 要素が表示されていません")
                browser.close()
                return False

        except Exception as e:
            print(f"❌ エラー: {e}")
            browser.close()
            return False

def main():
    print("=" * 60)
    print("Level X - Issue Y: [タイトル]")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_with_playwright()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### テストスクリプトのベストプラクティス

1. **明確なエラーメッセージ**: 学生が何を修正すべきか分かるように
2. **段階的なチェック**: 複数の条件を順番にチェック
3. **ファイル存在確認**: 対象ファイルが存在するか必ず確認
4. **コメント除外**: コメントアウトされたコードを無視する
5. **exit code**: 合格は0、不合格は1で終了

---

## トラブルシューティング

### よくある問題

#### 1. Dockerが起動しない
- Docker Desktopが起動しているか確認
- ポート3001が使用されていないか確認: `lsof -i :3001`

#### 2. データベースエラー
- `docker-compose down -v` で完全にクリーンアップ
- `data/` ディレクトリを削除して再起動

#### 3. Playwrightテストが失敗
- アプリケーションが起動しているか確認
- ブラウザがインストールされているか確認: `playwright install chromium`

#### 4. GitHub Actionsが動かない
- ワークフローファイルの構文エラーを確認
- ラベル名が正しいか確認
- Actionsタブでエラーログを確認

---

## バグの種類一覧

実装されているバグの種類：

### Level 1 (超初級) - 5点/問
- HTML/CSSのスペルミス・誤字
- タグの閉じ忘れ
- CSSプロパティの誤り（カラーコード、フォントサイズ）
- リンク先の誤り

### Level 2 (初級) - 10点/問
- JavaScriptの基本的なロジックバグ
- 計算ミス（Math.ceil/Math.floor/toFixed）
- フィルタリングの不具合
- イベントリスナーの設定ミス
- 日付フォーマットの問題

### Level 3 (中級) - 15点/問
- バリデーション不足（フロントエンド/バックエンド）
- エラーハンドリングの不備
- NULLチェック不足
- ワイルドカード検索の問題
- リソース削除時の関連処理漏れ

### Level 4 (上級) - 20点/問
- XSS脆弱性（エスケープ処理不足）
- SQLインジェクション
- 権限チェック不足

### Level 5 (最上級) - 25点/問
- トランザクション管理不備
- N+1クエリ問題
- リソースリーク（DB接続のクローズ忘れ）
- キャッシュ機構の欠如
- ファイル拡張子偽装対策

---

## まとめ

このプロジェクトは、学生が実践的なバグ修正を通じてWeb開発のスキルを習得できるように設計されています。

自動採点システムにより、学生は即座にフィードバックを受けられ、講師の採点負荷も大幅に軽減されます。

ご質問や改善提案がありましたら、お気軽にご連絡ください。
