# Issue一覧・点数配分表

本ドキュメントは、全issueの一覧と点数配分を記載したルールブックです。

## 📊 概要

| レベル | 問題数 | 各問の点数 | 合計点 | 内容 |
|--------|--------|-----------|--------|------|
| **Level 1 (超初級)** | 10問 | 5点 | 50点 | HTML/CSSの誤字・表記ミス |
| **Level 2 (初級)** | 10問 | 10点 | 100点 | JavaScriptの基本バグ |
| **Level 3 (中級)** | 10問 | 15点 | 150点 | バリデーション、エラーハンドリング |
| **Level 4 (上級)** | 5問 | 20点 | 100点 | セキュリティ脆弱性 |
| **Level 5 (最上級)** | 7問 | 25点 | 175点 | パフォーマンス、データ整合性 |
| **合計** | **42問** | - | **575点** | - |

---

## 📝 全Issue一覧表

### Level 1 - 超初級（HTML/CSS）

| Issue番号 | 問題の概要 | バグのジャンル | 該当ファイル | 点数 |
|-----------|------------|---------------|--------------|------|
| level_1/A | 特徴カードのタイトルに誤字（イベント上報満載） | HTML/CSS | frontend/promotion.html | 5 |
| level_1/B | 特徴カードのタイトルに誤字（リアルなユーザーレビユー） | HTML/CSS | frontend/promotion.html | 5 |
| level_1/C | 統計セクションのラベルに誤字（平均評化） | HTML/CSS | frontend/promotion.html | 5 |
| level_1/D | ボタンテキストに誤字（観光地一欄を見る） | HTML/CSS | frontend/promotion.html | 5 |
| level_1/E | フッターの著作権表示に誤字（群馬件観光ポータル） | HTML/CSS | frontend/promotion.html | 5 |
| level_1/F | メインタイトルのフォントサイズが極小（0.3rem） | HTML/CSS | frontend/promotion.html | 5 |
| level_1/G | ヒーローセクションの背景グラデーションが不正なカラーコード | HTML/CSS | frontend/promotion.html | 5 |
| level_1/H | 特徴カードのレイアウトが崩れ（閉じタグ不足） | HTML/CSS | frontend/promotion.html | 5 |
| level_1/I | ボタンリンク先が404エラー（spot.html → spots.html） | HTML/CSS | frontend/promotion.html | 5 |
| level_1/J | ボタンリンク先が404エラー（event.html → events.html） | HTML/CSS | frontend/promotion.html | 5 |

**Level 1 合計: 50点**

---

### Level 2 - 初級（JavaScript基本）

| Issue番号 | 問題の概要 | バグのジャンル | 該当ファイル | 点数 |
|-----------|------------|---------------|--------------|------|
| level_2/A | ランキングが0位から始まっている | JavaScript | frontend/stats.js | 10 |
| level_2/B | イベント開催日がデータベース形式のまま表示 | JavaScript | frontend/events.js | 10 |
| level_2/C | 距離フォーマット関数がundefinedを返す（return文なし） | JavaScript | frontend/api-client.js | 10 |
| level_2/D | 平均評価の小数点以下が長すぎる | JavaScript | frontend/spot-detail.js | 10 |
| level_2/E | 星評価の数が正しくない（Math.ceil使用） | JavaScript | frontend/spots.js | 10 |
| level_2/F | 未来の日付でチェックインできる | JavaScript | frontend/index.html | 10 |
| level_2/G | 検索結果件数が表示されない | JavaScript | frontend/events.js | 10 |
| level_2/H | 棒グラフの幅が正しく計算されていない | JavaScript | frontend/stats.js | 10 |
| level_2/I | 地域フィルターボタンが複数アクティブになる | JavaScript | frontend/spots.js | 10 |
| level_2/J | 画像拡大モーダルがESCキーで閉じない | JavaScript | frontend/spot-detail.js | 10 |

**Level 2 合計: 100点**

---

### Level 3 - 中級（バリデーション・エラーハンドリング）

| Issue番号 | 問題の概要 | バグのジャンル | 該当ファイル | 点数 |
|-----------|------------|---------------|--------------|------|
| level_3/A | YouTube動画の埋め込みが未実装 | JavaScript | frontend/index.html | 15 |
| level_3/B | 月別イベント取得APIで存在しない月のバリデーションなし | バックエンド | app/repositories/event_repository.py | 15 |
| level_3/C | ログアウト後もレビュー投稿フォームが表示される | JavaScript | frontend/spot-detail.js | 15 |
| level_3/D | レビュー投稿で星評価のJavaScriptバリデーションなし | JavaScript | frontend/spot-detail.js | 15 |
| level_3/E | レビュー投稿でレビュー内容のJavaScriptバリデーションなし | JavaScript | frontend/spot-detail.js | 15 |
| level_3/F | レビュー投稿APIに文字数制限がない | バックエンド | app/services/review_service.py | 15 |
| level_3/G | 統計APIでレビュー0件時の平均評価NULL処理なし | バックエンド | app/services/stats_service.py | 15 |
| level_3/H | 観光地検索でGLOBと%ワイルドカードの不適切な組み合わせ | バックエンド | app/repositories/spot_repository.py | 15 |
| level_3/I | イベントAPIにエラーハンドリングがない | バックエンド | app/controllers/event_controller.py | 15 |
| level_3/J | レビュー削除時に画像ファイルが削除されない | バックエンド | app/services/review_service.py | 15 |

**Level 3 合計: 150点**

---

### Level 4 - 上級（セキュリティ）

| Issue番号 | 問題の概要 | バグのジャンル | 該当ファイル | 点数 |
|-----------|------------|---------------|--------------|------|
| level_4/A | レビュー投稿機能にXSS脆弱性（review_content） | セキュリティ | frontend/spot-detail.js | 20 |
| level_4/B | イベント名表示にXSS脆弱性（event_name） | セキュリティ | frontend/events.js | 20 |
| level_4/C | レビュー削除APIに権限チェックの不備 | セキュリティ | app/services/review_service.py | 20 |
| level_4/D | イベント検索APIにSQLインジェクション脆弱性 | セキュリティ | app/repositories/event_repository.py | 20 |
| level_4/E | 統計APIのエリアフィルターにSQLインジェクション脆弱性 | セキュリティ | app/repositories/stats_repository.py | 20 |

**Level 4 合計: 100点**

---

### Level 5 - 最上級（パフォーマンス・データ整合性）

| Issue番号 | 問題の概要 | バグのジャンル | 該当ファイル | 点数 |
|-----------|------------|---------------|--------------|------|
| level_5/A | レビュー投稿処理のトランザクション管理不備 | パフォーマンス | app/services/review_service.py | 25 |
| level_5/B | 画像アップロード機能にファイル拡張子偽装対策不足 | セキュリティ | app/services/file_service.py | 25 |
| level_5/C | 観光地評価更新処理でデータベース接続のリソースリーク | パフォーマンス | app/repositories/spot_repository.py | 25 |
| level_5/D | レビュー表示時のN+1クエリ問題 | パフォーマンス | app/services/review_service.py | 25 |
| level_5/E | 月別イベント集計のGROUP BY句に不要なevent_id | バックエンド | app/repositories/stats_repository.py | 25 |
| level_5/F | 統計ページにキャッシュ機構がない | パフォーマンス | app/services/stats_service.py | 25 |
| level_5/G | イベント一覧で月別と地域別フィルターが同時使用不可 | JavaScript/バックエンド | frontend/events.js | 25 |

**Level 5 合計: 175点**

---

## 📈 バグジャンル別分類

| ジャンル | 問題数 | 合計点数 |
|---------|--------|---------|
| HTML/CSS | 10問 | 50点 |
| JavaScript | 13問 | 145点 |
| バックエンド（Python/SQL） | 9問 | 155点 |
| セキュリティ | 6問 | 125点 |
| パフォーマンス | 4問 | 100点 |

---


## 📖 各issueの詳細

各issueの詳細な説明、再現手順、ヒントは以下のディレクトリを参照してください：

- `issues/level_1/` - Level 1の各issue（A.md 〜 J.md）
- `issues/level_2/` - Level 2の各issue（A.md 〜 J.md）
- `issues/level_3/` - Level 3の各issue（A.md 〜 J.md）
- `issues/level_4/` - Level 4の各issue（A.md 〜 E.md）
- `issues/level_5/` - Level 5の各issue（A.md 〜 G.md）

各issueファイルには以下の情報が含まれています：

- 問題の詳細な説明
- 再現手順
- どうあるべきか（期待される動作）
- ヒント
- 自己採点方法（テストスクリプトの実行方法）
- プルリクエスト作成時のラベル

---

## 🔍 推奨される取り組み順序（例)

### 初心者向け
1. Level 1（A〜J）を全て解く → 50点獲得
2. Level 2（A〜E）を解く → 50点獲得
3. Level 3（A, C, D, E）を解く → 60点獲得
4. **合計: 160点**

### 中級者向け
1. Level 1を全てクリア → 50点
2. Level 2を全てクリア → 100点
3. Level 3を全てクリア → 150点
4. Level 4（A, B）を解く → 40点
5. **合計: 340点（銀賞相当）**

### 上級者向け
1. Level 1-3を全てクリア → 300点
2. Level 4を全てクリア → 100点
3. Level 5（A, D, E）を解く → 75点
4. **合計: 475点（金賞相当）**

---

## ⏱️ 推奨所要時間

| レベル | 1問あたりの目安 | レベル全体の目安 |
|--------|---------------|----------------|
| Level 1 | 5-10分 | 1-1.5時間 |
| Level 2 | 15-20分 | 2.5-3時間 |
| Level 3 | 30-45分 | 5-7時間 |
| Level 4 | 45-60分 | 4-5時間 |
| Level 5 | 60-90分 | 7-10時間 |

**全問解答の目安: 20-27時間**

実際の所要時間は個人のスキルレベルや経験によって大きく異なります。

---

## 📌 注意事項

- 各issueは独立しているため、どの順番で解いても構いません
- 1つのPull Requestには1つのissueの修正のみを含めてください
- 正しいラベル（例: `level_1/A`）を付けることで自動採点が実行されます
- 不合格の場合は何度でも再挑戦できます（ペナルティはありません）
- 詰まった場合は、issueドキュメントのヒントを参考にしてください

---

**最終更新日: 2025-12-15**
