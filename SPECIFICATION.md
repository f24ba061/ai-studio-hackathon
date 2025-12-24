# 群馬県観光地レビューアプリ - 詳細仕様書

## 📋 システム概要

### アプリケーションの目的
- 群馬県の観光地情報を提供するWebアプリケーション
- ユーザーが観光地にレビューを投稿できるプラットフォーム
- 学生向けWeb開発学習教材

### 技術スタック
- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **API**: REST API
- **アーキテクチャ**: 3層アーキテクチャ (Controller/Service/Repository)

## 🏗️ システム構成

### ファイル構成
```
ai-studio-hackathon/
├── app/                      # 3層アーキテクチャ版（現行）
│   ├── app.py               # メインアプリケーション
│   ├── config.py            # 設定ファイル
│   ├── controllers/         # Controller層
│   │   ├── spot_controller.py
│   │   ├── review_controller.py
│   │   └── user_controller.py
│   ├── services/            # Service層（ビジネスロジック）
│   │   ├── spot_service.py
│   │   ├── review_service.py
│   │   ├── user_service.py
│   │   └── file_service.py
│   ├── repositories/        # Repository層（データアクセス）
│   │   ├── database.py
│   │   ├── spot_repository.py
│   │   ├── review_repository.py
│   │   └── user_repository.py
│   └── models/              # Model層（未使用）
├── database/                # データベース関連
│   ├── schema.sql          # スキーマ定義
│   ├── add_tourist_spots.py
│   ├── add_sample_users.py
│   └── add_sample_reviews.py
├── frontend/                # フロントエンド
│   ├── index.html          # トップページ
│   ├── spots.html          # 観光地一覧
│   ├── spot-detail.html    # 観光地詳細
│   ├── credits.html        # クレジット
│   ├── styles.css          # スタイルシート
│   ├── api-client.js       # API通信クラス
│   ├── spots.js            # 一覧画面ロジック
│   ├── spot-detail.js      # 詳細画面ロジック
│   └── assets/             # 画像等の静的ファイル
│       └── images/
│           ├── spots/      # 観光地画像
│           ├── reviews/    # レビュー画像（ユーザー投稿）
│           └── placeholders/
└── tourism_review.db        # SQLiteデータベース
```

### アーキテクチャ
**3層アーキテクチャ**:
- **Controller層**: HTTPリクエスト/レスポンス処理、ルーティング
- **Service層**: ビジネスロジック、バリデーション
- **Repository層**: データベースアクセス、SQL実行

**起動方法**:
```bash
cd app
python3 app.py
```

## 🗄️ データベース仕様

### テーブル構成

#### 1. users テーブル（ユーザーマスター）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| user_id | INTEGER | PRIMARY KEY | ユーザーID（自動採番） |
| password | TEXT | NOT NULL | パスワード（平文保存・学習用） |
| name | TEXT | NOT NULL | ユーザー名 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新日時 |

**サンプルデータ**: 4ユーザー
- user_id: 1, name: テストユーザー, password: test123
- user_id: 2, name: 田中太郎, password: password456
- user_id: 3, name: 佐藤花子, password: mypass789
- user_id: 4, name: 鈴木一郎, password: secure321

#### 2. tourist_spots テーブル（観光地マスター）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| spot_id | INTEGER | PRIMARY KEY | 観光地ID（自動採番） |
| spot_name | TEXT | NOT NULL | 観光地名 |
| address | TEXT | | 住所 |
| access | TEXT | | アクセス情報 |
| business_hours | TEXT | | 営業時間 |
| fee | TEXT | | 料金 |
| map_url | TEXT | | Google Maps URL |
| description | TEXT | | 説明文 |
| avg_rating | REAL | DEFAULT 0 | 平均評価（自動計算） |
| review_count | INTEGER | DEFAULT 0 | レビュー数（自動計算） |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新日時 |

**サンプルデータ**: 21観光地
- 草津温泉、伊香保温泉、万座温泉、四万温泉、水上温泉
- 尾瀬、吹割の滝、榛名山・榛名湖、赤城山、妙義山
- 富岡製糸場、群馬サファリパーク、伊香保グリーン牧場
- 軽井沢おもちゃ王国、こんにゃくパーク、ロックハート城
- その他5ヶ所

#### 3. reviews テーブル（レビューデータ）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| review_id | INTEGER | PRIMARY KEY | レビューID（自動採番） |
| user_id | INTEGER | NOT NULL, FK | ユーザーID |
| spot_id | INTEGER | NOT NULL, FK | 観光地ID |
| review_content | TEXT | NOT NULL | レビュー内容 |
| rating | INTEGER | NOT NULL | 評価（1-5） |
| photo_filename | TEXT | | 画像ファイル名 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新日時 |

**制約**:
- UNIQUE(user_id, spot_id): 1ユーザー1観光地につき1レビューのみ
- FOREIGN KEY (user_id) REFERENCES users(user_id)
- FOREIGN KEY (spot_id) REFERENCES tourist_spots(spot_id)

#### 4. events テーブル（イベント情報）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| event_id | INTEGER | PRIMARY KEY | イベントID（自動採番） |
| event_name | TEXT | NOT NULL | イベント名 |
| event_date | TEXT | NOT NULL | 開催日（YYYY-MM-DD形式） |
| location | TEXT | | 開催場所 |
| area | TEXT | | 地域（maebashi, takasaki等） |
| category | TEXT | | カテゴリー（祭り、花火等） |
| description | TEXT | | イベント説明 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新日時 |

**サンプルデータ**: 20件
- 高崎だるま市（1月）
- 桐生八木節まつり（8月）
- 前橋花火大会（8月）
- 榛名湖花火大会（7月）
- 草津温泉感謝祭（5月、12月）
- その他各月イベント

### データベーストリガー

自動的に平均評価とレビュー数を更新するトリガーが設定されています。

#### 1. update_spot_rating_after_insert
レビュー追加時に観光地の平均評価とレビュー数を更新

#### 2. update_spot_rating_after_delete
レビュー削除時に観光地の平均評価とレビュー数を更新

#### 3. update_spot_rating_after_update
レビュー更新時に観光地の平均評価を更新

### ERD（Entity Relationship Diagram）
```
users (1) ────< reviews >──── (1) tourist_spots
  │               │                    │
  │               │                    │
  ├─ user_id (PK) ├─ review_id (PK)    ├─ spot_id (PK)
  ├─ password     ├─ user_id (FK)      ├─ spot_name
  ├─ name         ├─ spot_id (FK)      ├─ address
  ├─ created_at   ├─ review_content    ├─ access
  └─ updated_at   ├─ rating            ├─ business_hours
                  ├─ photo_filename    ├─ fee
                  ├─ created_at        ├─ map_url
                  └─ updated_at        ├─ description
                                       ├─ avg_rating ⭐
                                       ├─ review_count ⭐
                                       ├─ created_at
                                       └─ updated_at

⭐ = トリガーで自動更新される値
```

## 🔌 API仕様

### ベースURL
```
http://127.0.0.1:3001/api
```

### エンドポイント一覧

#### 観光地関連

##### GET /api/spots
観光地一覧を取得

**レスポンス例**:
```json
[
  {
    "spot_id": 1,
    "spot_name": "草津温泉",
    "address": "群馬県吾妻郡草津町草津",
    "access": "JR長野原草津口駅からバスで約25分",
    "business_hours": "24時間（施設により異なる）",
    "fee": "無料（一部施設有料）",
    "map_url": "https://maps.google.com/?q=草津温泉",
    "description": "日本三名泉の一つ...",
    "avg_rating": 4.5,
    "review_count": 3
  }
]
```

##### GET /api/spots/{spot_id}
特定の観光地を取得

**パラメータ**:
- `spot_id`: 観光地ID（整数）

**レスポンス**: 観光地オブジェクト（上記と同じ形式）

#### レビュー関連

##### GET /api/reviews/{spot_id}
特定観光地のレビュー一覧を取得

**パラメータ**:
- `spot_id`: 観光地ID（整数）

**レスポンス例**:
```json
[
  {
    "review_id": 1,
    "user_id": 1,
    "user_name": "テストユーザー",
    "spot_id": 1,
    "review_content": "素晴らしい温泉でした！",
    "rating": 5,
    "photo_filename": "review_1.jpg",
    "created_at": "2024-10-01 10:30:00"
  }
]
```

##### POST /api/reviews
レビューを投稿

**リクエスト形式**:
- Content-Type: `application/json` または `multipart/form-data`

**パラメータ（JSON）**:
```json
{
  "user_id": 1,
  "spot_id": 1,
  "review_content": "とても良かったです",
  "rating": 5
}
```

**パラメータ（FormData）**:
- `user_id`: ユーザーID
- `spot_id`: 観光地ID
- `review_content`: レビュー内容
- `rating`: 評価（1-5）
- `photo`: 画像ファイル（任意）

**レスポンス例**:
```json
{
  "success": true,
  "review_id": 42,
  "photo_filename": "review_42.jpg",
  "message": "レビューを投稿しました"
}
```

**エラーレスポンス例**:
```json
{
  "success": false,
  "error": "この観光地には既にレビューを投稿済みです。1つの観光地につき1つのレビューのみ投稿できます。"
}
```

##### DELETE /api/reviews/{review_id}
レビューを削除

**パラメータ**:
- `review_id`: レビューID（URL）
- `user_id`: ユーザーID（リクエストボディ）

**リクエスト例**:
```json
{
  "user_id": 1
}
```

**レスポンス例**:
```json
{
  "success": true,
  "message": "レビューを削除しました"
}
```

**エラーレスポンス例**:
```json
{
  "success": false,
  "error": "他のユーザーのレビューは削除できません"
}
```

#### 認証関連

##### POST /api/auth
ユーザー認証

**リクエスト**:
```json
{
  "user_id": "1",
  "password": "test123"
}
```

**レスポンス（成功）**:
```json
{
  "success": true,
  "user": {
    "user_id": 1,
    "name": "テストユーザー"
  }
}
```

**レスポンス（失敗）**:
```json
{
  "success": false,
  "message": "ユーザーIDまたはパスワードが正しくありません"
}
```

##### POST /api/users
ユーザー登録

**リクエスト**:
```json
{
  "password": "newpass123",
  "name": "新規ユーザー"
}
```

**レスポンス**:
```json
{
  "success": true,
  "user_id": 5,
  "message": "ユーザー登録が完了しました"
}
```

#### イベント関連

##### GET /api/events
イベント一覧を取得

**クエリパラメータ（任意）**:
- `month`: 月でフィルター（1〜12）
- `area`: 地域でフィルター（maebashi, takasaki等）

**レスポンス例**:
```json
[
  {
    "event_id": 1,
    "event_name": "高崎だるま市",
    "event_date": "2025-01-06",
    "location": "少林山達磨寺",
    "area": "takasaki",
    "category": "祭り",
    "description": "日本三大だるま市の一つ。境内に縁起だるまの露店が並び、多くの参拝者で賑わいます。",
    "created_at": "2025-01-01 00:00:00",
    "updated_at": "2025-01-01 00:00:00"
  }
]
```

##### GET /api/events?month=8
8月のイベントを取得

**レスポンス**: イベント配列（上記と同形式）

##### GET /api/events?area=maebashi
前橋地域のイベントを取得

**レスポンス**: イベント配列（上記と同形式）

##### GET /api/events/search?q={keyword}
イベントを検索

**クエリパラメータ**:
- `q`: 検索キーワード（イベント名、場所、説明から検索）

**レスポンス**: イベント配列（上記と同形式）

#### 静的ファイル配信

##### GET /
トップページ (`frontend/index.html`) を返す

##### GET /{filename}
`frontend/` ディレクトリ内の静的ファイルを配信

## 🎨 フロントエンド仕様

### ページ構成

#### 1. index.html（トップページ）
- アプリケーション紹介
- 主要観光地の紹介
- 観光地一覧へのリンク

#### 2. spots.html（観光地一覧）
- 全観光地のカード表示
- 平均評価・レビュー数の表示
- 詳細ページへのリンク

#### 3. spot-detail.html（観光地詳細）
- 観光地の詳細情報
- レビュー一覧表示
- レビュー投稿フォーム（ログイン時）
- レビュー削除ボタン（自分の投稿のみ）
- 画像クリックで拡大表示モーダル

#### 4. events.html（イベント一覧）
- イベントカード一覧表示
- 月別フィルター（1月〜12月）
- 地域別フィルター（前橋、高崎、草津など）
- キーワード検索機能
- 日付表示（月/日）

#### 5. credits.html（クレジット）
- 画像の出典情報

### JavaScript構成

#### api-client.js
APIクライアントクラス

**主要メソッド**:
- `getTouristSpots()`: 観光地一覧取得
- `getTouristSpot(spotId)`: 観光地詳細取得
- `searchTouristSpots(keyword)`: 観光地検索
- `getReviews(spotId)`: レビュー一覧取得
- `postReview(userId, spotId, reviewContent, rating)`: レビュー投稿
- `deleteReview(reviewId, userId)`: レビュー削除
- `authenticateUser(userId, password)`: ユーザー認証
- `registerUser(password, name)`: ユーザー登録
- `getEvents()`: イベント一覧取得
- `getEventsByMonth(month)`: 月別イベント取得
- `getEventsByArea(area)`: 地域別イベント取得
- `searchEvents(keyword)`: イベント検索

#### spots.js
観光地一覧画面のロジック

**主要機能**:
- 観光地データの読み込みと表示
- 星評価の視覚的表示

#### spot-detail.js
観光地詳細画面のロジック

**グローバル変数**:
- `isLoggedIn`: ログイン状態（boolean）
- `currentUser`: 現在のユーザー情報（object）
- `currentRating`: 現在選択中の評価
- `currentSpotId`: 現在表示中の観光地ID

**主要関数**:
- `loadUserFromStorage()`: LocalStorageからユーザー情報を復元
- `loadSpotDetails()`: 観光地詳細を取得・表示
- `loadReviews()`: レビュー一覧を取得・表示
- `handleLogin()`: ログイン処理
- `setRating(rating)`: 星評価を設定
- `submitReview(event)`: レビュー投稿処理
- `deleteReview(reviewId)`: レビュー削除処理
- `showImageModal(imageSrc)`: 画像拡大モーダル表示
- `closeImageModal()`: モーダルを閉じる

#### events.js
イベント一覧画面のロジック

**グローバル変数**:
- `allEvents`: 全イベントデータ（配列）
- `currentFilter`: 現在適用中のフィルター（object）

**主要関数**:
- `loadEventsFromDatabase()`: イベントデータの読み込み
- `displayEvents(events)`: イベント一覧の表示
- `filterByMonth(month, clickedButton)`: 月別フィルタリング
- `filterByArea(area, clickedButton)`: 地域別フィルタリング
- `searchEvents()`: キーワード検索
- `clearSearch()`: 検索クリア

### スタイリング

#### styles.css
- レスポンシブデザイン（モバイル対応）
- 星評価の視覚的表示
- カードレイアウト
- モーダルダイアログ
- フォームスタイリング

## ⚙️ 主要機能詳細

### 1. 認証機能

**実装場所**:
- Backend: `app/services/user_service.py`
- Frontend: `frontend/spot-detail.js` L144-176

**フロー**:
1. ユーザーがユーザーIDとパスワードを入力
2. `/api/auth` にPOSTリクエスト
3. バックエンドでユーザー認証
4. 成功時、ユーザー情報をLocalStorageに保存
5. `isLoggedIn = true`, `currentUser` に情報を格納

**ログイン状態の保持**:
- LocalStorage キー: `'currentUser'`
- ページリロード時に `loadUserFromStorage()` で復元

**テストアカウント**:
```
ユーザーID: 1
パスワード: test123
名前: テストユーザー
```

### 2. レビュー投稿機能

**実装場所**:
- Backend: `app/services/review_service.py`
- Frontend: `frontend/spot-detail.js` L194-263

**バリデーション**:
1. ログイン必須チェック
2. 評価（1-5）必須チェック
3. レビュー内容の空欄チェック
4. 既存レビューの重複チェック（1ユーザー1観光地1レビュー）
5. 画像形式・サイズチェック（任意）

**画像アップロード**:
- 対応形式: JPEG, PNG, GIF
- 最大サイズ: 5MB
- 保存先: `frontend/assets/images/reviews/`
- ファイル名: `review_{review_id}.{拡張子}`

**処理フロー**:
1. フロントエンドでバリデーション
2. 画像がある場合は FormData、ない場合は JSON で送信
3. バックエンドで重複チェック
4. レビュー作成
5. 画像保存（ある場合）
6. トリガーで平均評価・レビュー数を自動更新
7. フロントエンドで一覧を再読み込み

### 3. レビュー削除機能

**実装場所**:
- Backend: `app/services/review_service.py` L86-109
- Frontend: `frontend/spot-detail.js` L266-292

**権限制御**:
- 自分が投稿したレビューのみ削除可能
- `review.user_id === currentUser.user_id` でチェック
- バックエンドでも二重チェック

**削除ボタンの表示条件**:
```javascript
const deleteButtonHtml = (currentUser && Number(review.user_id) === Number(currentUser.user_id))
    ? `<button onclick="deleteReview(${review.review_id})">削除</button>`
    : '';
```

**処理フロー**:
1. 削除ボタンクリック
2. 確認ダイアログ表示
3. `/api/reviews/{review_id}` に DELETE リクエスト
4. バックエンドで権限チェック
5. 画像ファイル削除（存在する場合）
6. レビュー削除
7. トリガーで平均評価・レビュー数を自動更新
8. フロントエンドで一覧を再読み込み

### 4. レビュー重複制限機能

**実装方針**:
- データベースレベル: UNIQUE(user_id, spot_id) 制約
- サービスレベル: `find_by_user_and_spot()` でチェック
- フロントエンドレベル: 既存レビューの有無を確認

**実装場所**:
- Database: `tourism_review.db` reviews テーブル
- Backend: `app/services/review_service.py` L26-35, L62-68
- Backend: `app/repositories/review_repository.py` L113-131
- Frontend: `frontend/spot-detail.js` L217-227

**エラーメッセージ**:
```
この観光地には既にレビューを投稿済みです。1つの観光地につき1つのレビューのみ投稿できます。
```

### 5. 画像表示・拡大機能

**実装場所**:
- Frontend: `frontend/spot-detail.js` L107-113, L294-333

**表示仕様**:
- サムネイル: 最大250px
- クリックで拡大モーダル表示
- モーダル内: 最大90%サイズ
- 背景クリックまたはESCキーで閉じる

**モーダル実装**:
```javascript
function showImageModal(imageSrc) {
    // モーダルHTMLを動的生成
    // position: fixed で全画面表示
    // background: rgba(0, 0, 0, 0.9) で半透明背景
}

function closeImageModal() {
    // モーダル要素を削除
}

// ESCキーで閉じる
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeImageModal();
    }
});
```

### 6. 平均評価・レビュー数の自動更新

**実装方式**: データベーストリガー

**更新タイミング**:
- レビュー追加時（INSERT）
- レビュー削除時（DELETE）
- レビュー更新時（UPDATE）

**計算ロジック**:
```sql
-- 平均評価
avg_rating = AVG(rating) FROM reviews WHERE spot_id = {spot_id}

-- レビュー数
review_count = COUNT(*) FROM reviews WHERE spot_id = {spot_id}
```

**表示形式**:
- フロントエンド: `toFixed(1)` で小数点第1位まで表示
- 例: 4.25 → "4.3"

## 🔧 設定・環境

### サーバー設定

**app/config.py**:
```python
class Config:
    # プロジェクトルートの絶対パス
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # データベース
    DB_NAME = os.path.join(PROJECT_ROOT, 'tourism_review.db')

    # ファイルアップロード
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'frontend', 'assets', 'images', 'reviews')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # フロントエンド
    FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
```

**サーバー起動設定**:
- ポート: 3001
- ホスト: 127.0.0.1
- デバッグモード: True（学習用）
- CORS: 全オリジン許可（学習用）

### データベース設定

**ファイル**: `tourism_review.db`
**場所**: プロジェクトルート
**文字エンコーディング**: UTF-8
**接続設定**: `repositories/database.py`

```python
def get_db():
    conn = sqlite3.connect(Config.DB_NAME)
    conn.row_factory = sqlite3.Row  # 辞書形式でアクセス可能
    return conn
```

## 🚀 セットアップ手順

### 1. 依存関係のインストール
```bash
pip install flask flask-cors
```

### 2. データベース初期化
```bash
# 初期化スクリプトを使用（推奨）
python3 database/init_db.py

# サンプルデータ投入
python3 database/add_tourist_spots.py
python3 database/add_sample_users.py
python3 database/add_sample_reviews.py
python3 database/add_sample_events.py
```

### 3. サーバー起動
```bash
cd app
python3 app.py
```

### 4. アクセス
ブラウザで http://127.0.0.1:3001 を開く

## 🐛 デバッグ・トラブルシューティング

### よくあるエラー

#### 1. データベースファイル未作成
```
sqlite3.OperationalError: no such table: users
```
**対処法**: スキーマファイルを実行してテーブル作成
```bash
sqlite3 tourism_review.db < database/schema.sql
```

#### 2. ポート競合
```
OSError: [Errno 48] Address already in use
```
**対処法**: 既存のプロセスを終了
```bash
lsof -ti:3001 | xargs kill -9
```

#### 3. モジュール未インストール
```
ModuleNotFoundError: No module named 'flask'
```
**対処法**:
```bash
pip install flask flask-cors
```

#### 4. トリガーが動作しない
**症状**: レビュー追加・削除後も平均評価が更新されない
**対処法**: トリガーを再作成
```bash
sqlite3 tourism_review.db "SELECT name FROM sqlite_master WHERE type='trigger';"
# トリガーが表示されない場合は再作成が必要
```

#### 5. 画像が表示されない
**対処法**:
- 画像ファイルのパスを確認
- `frontend/assets/images/spots/` に画像が存在するか確認
- `frontend/assets/images/placeholders/no-image.png` が存在するか確認

### 確認コマンド

**データベース内容確認**:
```bash
sqlite3 tourism_review.db
.tables
SELECT * FROM users;
SELECT * FROM tourist_spots LIMIT 5;
SELECT COUNT(*) FROM reviews;
SELECT spot_name, avg_rating, review_count FROM tourist_spots;
```

**トリガー確認**:
```bash
sqlite3 tourism_review.db "SELECT name FROM sqlite_master WHERE type='trigger';"
```

**サーバーログ確認**: デバッグモードで詳細ログが表示されます

## 📚 バリデーション仕様

### フロントエンドバリデーション

**レビュー投稿時**:
1. ログイン状態チェック
2. 評価が0でないことをチェック
3. レビュー内容が空でないことをチェック
4. 既存レビューの重複チェック

**ログイン時**:
1. ユーザーIDの入力チェック
2. パスワードの入力チェック

### バックエンドバリデーション

**レビュー投稿時** (`review_service.py`):
1. 必須フィールドチェック（user_id, spot_id, review_content, rating）
2. 重複チェック（同一ユーザー・同一観光地）
3. 画像ファイルのバリデーション（形式・サイズ）

**レビュー削除時** (`review_service.py`):
1. レビューの存在チェック
2. 権限チェック（投稿者本人のみ削除可能）

**ユーザー認証時** (`user_service.py`):
1. ユーザーIDの存在チェック
2. パスワードの一致チェック

### 画像ファイルバリデーション

**許可される形式**: PNG, JPG, JPEG, GIF
**最大サイズ**: 5MB

**バリデーション実装** (`file_service.py`):
```python
def validate_image(self, file):
    if not file or not file.filename:
        return None

    # 拡張子チェック
    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext not in Config.ALLOWED_EXTENSIONS:
        return '画像ファイルはPNG、JPG、GIF形式のみ対応しています'

    # ファイルサイズチェック（5MB）
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > Config.MAX_CONTENT_LENGTH:
        return 'ファイルサイズは5MB以下にしてください'

    return None
```

## 📊 データ仕様

### 群馬県観光地データ（16ヶ所）

**温泉地**:
1. 草津温泉
2. 伊香保温泉
3. 万座温泉
4. 四万温泉
5. 水上温泉

**自然景観**:
6. 尾瀬
7. 吹割の滝
8. 榛名山・榛名湖
9. 赤城山
10. 妙義山

**観光施設**:
11. 富岡製糸場（世界遺産）
12. 群馬サファリパーク
13. 伊香保グリーン牧場
14. 軽井沢おもちゃ王国
15. こんにゃくパーク
16. ロックハート城

### サンプルユーザー（4名）

| user_id | name | password |
|---------|------|----------|
| 1 | テストユーザー | test123 |
| 2 | 田中太郎 | password456 |
| 3 | 佐藤花子 | mypass789 |
| 4 | 鈴木一郎 | secure321 |

### サンプルレビュー

各観光地に0〜4件のレビューが投稿されています。
詳細は `database/add_sample_reviews.py` を参照。

## 📝 学習用途について

このアプリケーションは学生向けのWeb開発学習教材として設計されています。

### 学習目標

1. **Web開発の基礎理解**
   - HTML/CSS/JavaScriptの連携
   - REST APIの概念と実装
   - データベース操作（CRUD）
   - 3層アーキテクチャの理解

2. **デバッグスキルの向上**
   - ブラウザ開発者ツールの使用
   - エラーログの読み方
   - 問題の切り分け方法

3. **セキュリティ意識の向上**
   - 入力値検証の重要性
   - パスワード管理のベストプラクティス
   - ファイルアップロードのセキュリティ

### 仕込み可能なバグの例

#### 簡単（10個程度）
1. 星評価が0のまま投稿できる
2. レビュー内容が空でも投稿できる
3. 画像拡大モーダルが閉じない
4. 平均評価の表示桁数が多すぎる
5. 削除ボタンの表示条件ミス
6. ログアウト後もレビュー投稿できる
7. 存在しない観光地IDでエラーが出ない
8. 画像ファイルサイズチェック漏れ
9. レビュー削除後に一覧が更新されない
10. エラーメッセージが表示されない

#### 中級（5個程度）
1. 同じ観光地に複数レビュー投稿できる（UNIQUE制約削除）
2. トリガーが動作せず平均評価が更新されない
3. 他人のレビューを削除できる（権限チェック不備）
4. SQLインジェクション脆弱性
5. XSS脆弱性（レビュー内容のエスケープ漏れ）

#### 上級（5個程度）
1. セッション管理の不備
2. ファイルアップロードの脆弱性（任意ファイル実行）
3. CSRF脆弱性
4. データベーストランザクション処理の不備
5. 競合状態（レースコンディション）

### セキュリティ上の注意（意図的な簡略化）

このアプリケーションは学習目的のため、以下のセキュリティ対策を意図的に簡略化しています：

1. **パスワード平文保存**: 本番環境ではハッシュ化必須
2. **CORS設定が緩い**: `*` で全許可
3. **セッション管理なし**: LocalStorageのみ
4. **入力値検証が簡易的**: より厳密な検証が必要

## 🤝 貢献

このプロジェクトは教育目的で作成されています。改善提案やバグ報告は歓迎します。

## 📄 ライセンス

MIT License

---

**最終更新日**: 2024年10月3日
**バージョン**: 1.0
**対象**: 学生向けWeb開発学習教材
