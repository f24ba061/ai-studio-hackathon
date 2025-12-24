# 群馬県観光地レビューアプリ

学生向けバグ修正教材として作成されたWebアプリケーションです。Python Flask + SQLiteを使用しています。

## 🚀 セットアップ手順

### Docker環境（必須）

このプロジェクトは**Docker環境での実行が必須**です。GitHub Actionsによる自動採点もDocker環境を前提としています。

#### 前提条件
- **Docker Desktop** または **Docker** がインストールされていること
  - [Docker Desktop ダウンロード](https://www.docker.com/products/docker-desktop/)

#### 起動方法
```bash
# リポジトリをクローンまたはテンプレートから作成
git clone <your-repository-url>
cd ai-studio-hackathon

# イメージをビルドして起動
docker compose up --build

# バックグラウンドで起動する場合（推奨）
docker compose up -d

# ログを確認する場合
docker compose logs -f

# 停止する場合
docker compose down
```

#### ブラウザでアクセス
アプリケーションが起動したら、以下のURLにアクセスできます：
- **メイン**: http://localhost:3001
- **観光スポット**: http://localhost:3001/spots.html
- **イベント情報**: http://localhost:3001/events.html
- **統計ページ**: http://localhost:3001/stats.html

**注意**:
- データベースは `./data/` ディレクトリに永続化されます
- 初回起動時に自動的に初期化され、サンプルデータが投入されます
- アプリケーションはポート **3001** で動作します（自動採点でも同じポートを使用）

#### データベースを再初期化する場合
```bash
# コンテナとボリュームを削除
docker compose down -v

# 再起動（自動的にデータベースが初期化されます）
docker compose up -d
```

#### トラブルシューティング
- **ポート3001が既に使用されている**: 他のアプリケーションを停止してください
- **Dockerが起動しない**: Docker Desktopが起動していることを確認してください
- **データベースエラー**: `docker compose down -v` で完全にクリーンアップしてから再起動してください

## 🔑 テスト用ログイン情報
- **ユーザーID**: 1
- **パスワード**: test123

## 🛠️ 主な機能
- 群馬県観光地の一覧表示・検索
- 地域別フィルタリング
- 観光地詳細ページ
- レビューの投稿・表示（画像添付可能）
- ユーザーログイン機能
- イベント情報の表示・検索
- 月別・地域別イベントフィルタリング
- 統計ページ

## 🐛 学習の進め方

### 実装済みバグ問題: 合計42問

| 難易度 | 問題数 | 内容 |
|--------|--------|------|
| **超初級 (level_1)** | 10問 | HTML/CSSの基本的なミス |
| **初級 (level_2)** | 10問 | JavaScriptの基本バグ |
| **中級 (level_3)** | 10問 | バリデーション、エラーハンドリング |
| **上級 (level_4)** | 5問 | セキュリティ脆弱性（XSS、SQLインジェクション等） |
| **最上級 (level_5)** | 7問 | パフォーマンス、データ整合性 |

各バグの詳細は `issues/level_1/` 〜 `issues/level_5/` フォルダを参照してください。

### 学習フロー

#### 1. 環境セットアップ
1. このテンプレートから自分のリポジトリを作成
2. ローカルにクローン
3. Docker環境でアプリケーションを起動
4. 各機能を試して動作を確認

#### 2. バグ修正の基本フロー
1. **issueを選ぶ**: `issues/`フォルダから修正するバグを選ぶ
2. **ブランチを作成**: `git checkout -b fix/level_X-Y`
3. **バグを再現**: issueに記載された手順でバグを再現する
4. **コードを理解**: ファイル構成を確認し、該当箇所を特定する
5. **バグを修正**: ヒントを参考に原因を特定し、修正する
6. **動作確認**: Docker環境で修正後の動作を確認する
7. **コミット**: `git add .` → `git commit -m "Fix level_X/Y: 説明"`
8. **プッシュ**: `git push origin fix/level_X-Y`

#### 3. GitHub自動採点システム
1. **Pull Requestを作成**: GitHubでdevelopブランチに向けてPRを作成
2. **ラベルを付与**: PRに `level_X/Y` のラベルを付ける（例: `level_1/A`）
3. **自動テストが実行**: GitHub Actionsが自動的にテストを実行
4. **結果を確認**:
   - ✅ **合格**: PRにコメントで「合格」が通知される
   - ❌ **不合格**: PRにコメントで「不合格」とヒントが表示される
5. **再挑戦**: 不合格の場合は修正して再度プッシュ、ラベルを付け直す

**重要**:
- 自動採点はDocker環境（`localhost:3001`）を前提としています
- ラベルを付けるたびにテストが実行されます
- 1つのPRで複数のissueを修正しないでください（1PR = 1issue）

#### 4. 利用可能なラベル
- `level_1/A` 〜 `level_1/J` (10個)
- `level_2/A` 〜 `level_2/J` (10個)
- `level_3/A` 〜 `level_3/J` (10個)
- `level_4/A` 〜 `level_4/E` (5個)
- `level_5/A` 〜 `level_5/G` (7個)

## 📚 さらに詳しく知りたい場合

プロジェクトの詳細な構成や技術情報は [README_INSTRUCTOR.md](./README_INSTRUCTOR.md) を参照してください。

## 📝 技術スタック
- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **API**: REST API
- **Infrastructure**: Docker

---

頑張ってバグを修正しましょう！🚀
