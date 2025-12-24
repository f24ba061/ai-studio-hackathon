<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
POST /api/reviews

## 問題の簡単な説明 (Explain the problem):
レビュー投稿処理にトランザクション（複数の処理を1つのまとまりとして扱い、全て成功するか全て失敗するかのどちらかにする仕組み）管理の不備があります。レビューの作成には成功したが画像の保存に失敗した場合、レビューデータだけがデータベースに残り、画像ファイルが存在しない不整合な状態になります。

## どうあるべきか (To be):
 - レビュー作成と画像保存は、一連のトランザクションとして処理されるべきです。
 - どちらか一方が失敗した場合、両方がロールバックされる必要があります。
 - データベースとファイルシステムの整合性が保たれるべきです。

## 再現する手順 (Steps to reproduce the problem):
 1. 画像保存先のディレクトリの権限を変更して、書き込み不可にする
    ```bash
    chmod 000 frontend/assets/images/reviews/
    ```
 2. ブラウザで `/spot-detail.html?id=1` にアクセスする
    （既にユーザー4がspot_id=1にレビュー投稿済みの場合は、別の観光地を選んでください）
 3. ログインして（ユーザーID: 4, パスワード: password789）、画像を添付したレビューを投稿する
 4. 「レビューを投稿しました」という成功メッセージが表示される（ユーザーは成功したと思う）
 5. データベースを確認すると、レビューは作成されているが、photo_filenameは空になっている
    ```bash
    sqlite3 data/tourism_review.db "SELECT review_id, user_id, spot_id, photo_filename FROM reviews ORDER BY review_id DESC LIMIT 1;"
    ```
 6. 画像保存に失敗したにも関わらず、エラーが握りつぶされて成功として処理されている
 7. ユーザーは画像付きでレビューを投稿したつもりだが、実際には画像なしのレビューになっている
 8. 権限を元に戻す:
    ```bash
    chmod 755 frontend/assets/images/reviews/
    ```

## その他の情報 (Other information):
**該当コード箇所:**
`app/services/review_service.py` 112-115行目付近

```python
def create_review(self, review_data):
    # レビューを作成
    review_id = self.review_repo.create(review_data)

    # トランザクション処理不備
    # 画像保存失敗時にレビューをロールバックしていない
    # 本来はトランザクションを使って、画像保存失敗時はレビューも削除すべき

    # 画像がある場合は保存
    if review_data.get('photo'):
        photo = review_data['photo']
        result = self.file_service.save_review_photo(photo, review_id)
        # ...
```

**ヒント:**
- データベーストランザクション（複数の処理を1つのまとまりとして扱う仕組み）を使用して、レビュー作成と画像保存を一つの単位として扱う必要があります
- 画像保存に失敗した場合、作成したレビューを削除する処理を追加する方法もあります
- 例:
  ```python
  try:
      review_id = self.review_repo.create(review_data)
      if review_data.get('photo'):
          result = self.file_service.save_review_photo(photo, review_id)
          if not result['success']:
              self.review_repo.delete(review_id)  # ロールバック
              return result
  except Exception as e:
      # エラー処理
  ```

**参考URL:**
- https://www.sqlite.org/lang_transaction.html

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_5/A`

**PRタイトル例:**
```
[Level 5-A] 問題の簡単な説明
```
