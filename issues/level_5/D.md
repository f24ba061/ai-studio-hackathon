<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
GET /api/reviews/{spot_id}

## 問題の簡単な説明 (Explain the problem):
レビュー表示時にN+1クエリ問題（1回で取得できるデータを何度も繰り返し取得してしまう問題）が発生しています。レビューが100件ある場合、レビュー取得に1回 + 各レビューのユーザー名取得に100回 = 合計101回のSQLクエリが発行され、パフォーマンスが大幅に低下します。

## どうあるべきか (To be):
 - レビューとユーザー情報は、JOIN句を使って1回のクエリで取得されるべきです。
 - データベースへのアクセス回数を最小限に抑える必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. 観光地に大量のレビュー（20件以上）を投稿する
 2. Flaskアプリケーションで、SQLクエリのログを有効にする
 3. ブラウザで `/spot-detail.html?id=1` にアクセスする
 4. サーバーのログを確認し、レビュー数+1回のSELECT文が実行されていることを確認
 5. ページの読み込みが遅いことを体感する

## その他の情報 (Other information):
**該当コード箇所:**

**サービス層** `app/services/review_service.py` 14-29行目:
```python
def get_reviews_by_spot(self, spot_id):
    user_repo = UserRepository()

    # N+1クエリ問題
    reviews = self.review_repo.find_by_spot_id(spot_id)

    # 各レビューにユーザー名を追加（N回のクエリが発生）
    for review in reviews:
        user = user_repo.find_by_id(review['user_id'])  # ← ループ内でクエリ
        review['user_name'] = user['name'] if user else '不明'

    return reviews
```

**リポジトリ層** `app/repositories/review_repository.py` 17-20行目:
```python
def find_by_spot_id(self, spot_id):
    conn = get_db()
    cursor = conn.cursor()

    # N+1クエリ問題
    # JOINを使っていないため、ユーザー情報が取得できない
    cursor.execute('''
        SELECT *
        FROM reviews
        WHERE spot_id = ?
        ORDER BY created_at DESC
    ''', (spot_id,))
    # ...
```

**ヒント:**
- SQL JOIN句を使って、レビューとユーザー情報を一度に取得しましょう
- 例:
  ```python
  cursor.execute('''
      SELECT r.*, u.name as user_name
      FROM reviews r
      LEFT JOIN users u ON r.user_id = u.user_id
      WHERE r.spot_id = ?
      ORDER BY r.created_at DESC
  ''', (spot_id,))
  ```
- サービス層でのループ処理が不要になります

**参考URL:**
- https://stackoverflow.com/questions/97197/what-is-the-n1-selects-problem-in-orm-object-relational-mapping

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_5/D`

**PRタイトル例:**
```
[Level 5-D] 問題の簡単な説明
```
