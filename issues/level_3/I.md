<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
GET /api/events

## 問題の簡単な説明 (Explain the problem):
イベントAPI（イベントデータを取得する仕組み）のエラー処理が実装されていません。データベースエラーなどの例外が発生した場合、500エラーのスタックトレース（エラーの詳細情報）がそのままクライアント（利用者）に返されてしまいます。

## どうあるべきか (To be):
 - エラーが発生した場合、詳細なスタックトレースではなく、ユーザーに分かりやすいエラーメッセージが返されるべきです。
 - サーバーの内部情報が露出しないようにする必要があります。
 - エラーの詳細はサーバーログ（記録）に記録し、クライアントには安全なメッセージのみを返すべきです。

## 確認方法 (How to verify):
このissueはコードレビューで発見されました。以下の方法で問題を確認できます：

 1. `app/controllers/event_controller.py` の `get_events()` 関数と `search_events()` 関数を確認
 2. try-exceptブロックが実装されていないことを確認
 3. 例外が発生した場合、Flaskのデフォルトエラーハンドリングにより、デバッグモードではスタックトレースが露出することを理解する

## その他の情報 (Other information):
**該当コード箇所:**
`app/controllers/event_controller.py` 10-30行目付近

```python
@events_bp.route('/events', methods=['GET'])
def get_events():
    # エラーハンドリングが実装されていない
    month = request.args.get('month')
    area = request.args.get('area')

    if month:
        events = event_service.get_events_by_month(month)
    elif area:
        events = event_service.get_events_by_area(area)
    else:
        events = event_service.get_all_events()

    return jsonify(events)
```

**ヒント:**
- try-exceptブロック（エラーを捕捉する仕組み）でエラーをキャッチする必要があります
- エラーが発生した場合、詳細なスタックトレースではなく、ユーザーに分かりやすいメッセージを返しましょう
- 例: `return jsonify({'error': 'イベントの取得に失敗しました'}), 500`
- セキュリティ上、内部エラーの詳細を外部に公開しないことが重要です

※jsonify: PythonのデータをJSON形式に変換する関数

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_3/I`

**PRタイトル例:**
```
[Level 3-I] 問題の簡単な説明
```
