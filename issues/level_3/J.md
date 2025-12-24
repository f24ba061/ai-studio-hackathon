<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
DELETE /api/reviews/{review_id}

## 問題の簡単な説明 (Explain the problem):
レビューを削除しても、そのレビューに添付されていた画像ファイルがサーバーのディスク上に残ったままになります。

## どうあるべきか (To be):
 - レビュー削除時に、そのレビューに添付されていた画像ファイルも一緒に削除されるべきです。
 - 不要なファイルがディスクを圧迫しないようにする必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. ブラウザで `/spot-detail.html?id=1` にアクセスする
 2. ログインする（ユーザーID: 4, パスワード: password789）
 3. レビュー投稿フォームで、星評価とレビュー内容を入力し、画像ファイルを選択して投稿する
 4. Finderまたはターミナルで `frontend/assets/images/reviews/` フォルダを開き、画像ファイルが保存されていることを確認する
    - ファイル名は `review_{レビューID}.{拡張子}` の形式（例: `review_15.jpg`）
 5. 投稿したレビューの「削除」ボタンをクリックして、レビューを削除する
 6. 再度 `frontend/assets/images/reviews/` フォルダを確認する
 7. レビューはデータベースから削除されているが、画像ファイルは削除されずに残っていることを確認

## その他の情報 (Other information):
**該当コード箇所:**
`app/services/review_service.py` 136-139行目付近

```python
def delete_review(self, review_id, user_id):
    review = self.review_repo.find_by_id(review_id)
    # ...権限チェック...

    # 画像ファイルの削除処理が実装されていない

    # レビューをデータベースから削除
    result = self.review_repo.delete(review_id)
    # ...
```

**ヒント:**
- レビューに画像が添付されている場合、データベースから削除する前にファイルも削除する必要があります
- `review.get('photo_filename')` で画像ファイル名を確認できます
- `file_service.delete_review_photo(filename)`メソッド（画像を削除する機能）を呼び出して、物理ファイルを削除しましょう
- データとファイルの整合性（一致）を保つことが重要です

※メソッド: オブジェクトに用意されている機能

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_3/J`

**PRタイトル例:**
```
[Level 3-J] 問題の簡単な説明
```
