<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
GET /api/stats/summary

## 問題の簡単な説明 (Explain the problem):
統計API（統計データを取得する仕組み）で、レビューが0件の場合に平均評価がNULL（値が存在しない状態）となり、エラーが発生します。

## どうあるべきか (To be):
 - レビューが0件の場合、平均評価は0または適切なデフォルト値（初期値）として扱われるべきです。
 - NULL値を適切に処理して、エラーが発生しないようにする必要があります。

## 確認方法 (How to verify):
このissueはコードレビューで発見されました。以下の方法で問題を確認できます：

 1. `app/services/stats_service.py` の `get_summary()` 関数を確認
 2. 26行目で `avg_rating_overall` に対してNULLチェックなしで `round()` を実行していることを確認
 3. データベースにレビューが存在しない場合、`avg_rating_overall` がNULLとなり、`round(None, 1)` でTypeErrorが発生することを理解する

## その他の情報 (Other information):
**該当コード箇所:**
`app/services/stats_service.py` 28-29行目付近

```python
def get_summary(self):
    summary = self.repository.fetch_summary()
    # ...（省略）

    # NULL値チェックが実装されていない
    # avg_rating_overall が NULL の場合、round() でエラーが発生
    summary['avg_rating_overall'] = round(summary['avg_rating_overall'], 1)

    return summary
```

**ヒント:**
- `avg_rating_overall`がNULLでないかチェックしてから処理する必要があります
- 例:
  ```python
  if summary['avg_rating_overall'] is not None:
      summary['avg_rating_overall'] = round(summary['avg_rating_overall'], 1)
  else:
      summary['avg_rating_overall'] = 0
  ```
- SQLのCOALESCE関数（NULLの場合に別の値を使う機能）を使ってリポジトリ層（データベース操作を行う部分）で対応する方法もあります

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_3/G`

**PRタイトル例:**
```
[Level 3-G] 問題の簡単な説明
```
