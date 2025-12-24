<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
GET /api/stats/events-by-month

## 問題の簡単な説明 (Explain the problem):
月別イベント集計のSQLクエリで、GROUP BY句に不要な`event_id`が含まれているため、正しく集計されません。各イベントが個別の行として扱われ、月ごとの合計が計算されません。

## どうあるべきか (To be):
 - GROUP BY句には、集計の基準となる月のみを指定するべきです。
 - 各月のイベント数が正しく合計されて返される必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. ブラウザで `/stats.html` にアクセスする
 2. 「月別イベント開催数」のグラフを確認する
 3. 各月の件数が実際よりも少なく表示されていることを確認
 4. ブラウザの開発者ツールでAPIレスポンスを確認:
    ```javascript
    fetch('http://127.0.0.1:3001/api/stats/events-by-month')
      .then(r => r.json())
      .then(console.log)
    ```
 5. 同じ月に複数のイベントがあっても、正しく合計されていないことを確認

## その他の情報 (Other information):
**該当コード箇所:**
`app/repositories/stats_repository.py` 122-130行目付近

```python
def fetch_events_by_month(self):
    conn = get_db()
    cursor = conn.cursor()

    # GROUP BY にevent_idを含めると、1行1イベントになり集計されない
    cursor.execute('''
        SELECT
            CAST(substr(event_date, 6, 2) AS INTEGER) as month,
            COUNT(*) as count
        FROM events
        GROUP BY month, event_id  # ← event_idが不要
        ORDER BY month
    ''')
    # ...
```

**ヒント:**
- `GROUP BY month, event_id` を `GROUP BY month` に修正しましょう
- `event_id`を含めると、各イベントが個別にグループ化されてしまい、月ごとの合計が計算されません
- 修正後:
  ```python
  cursor.execute('''
      SELECT
          CAST(substr(event_date, 6, 2) AS INTEGER) as month,
          COUNT(*) as count
      FROM events
      GROUP BY month
      ORDER BY month
  ''')
  ```

**参考URL:**
- https://www.sqlite.org/lang_select.html#resultset

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_5/E`

**PRタイトル例:**
```
[Level 5-E] 問題の簡単な説明
```
