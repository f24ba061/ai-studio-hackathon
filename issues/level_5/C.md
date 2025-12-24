<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
GET /api/spots/{spot_id}

## 問題の簡単な説明 (Explain the problem):
観光地の平均評価を更新する処理で、データベース接続のリソースリークが発生しています。接続を適切に閉じていないため、長時間運用すると接続が枯渇し、新しいリクエストを処理できなくなります。

## どうあるべきか (To be):
 - データベース接続は、使用後に必ず閉じられるべきです。
 - エラーが発生した場合でも、`finally`句で確実に接続を解放する必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. 大量のレビューを投稿するスクリプトを実行する（100回以上）
 2. データベース接続数を監視する
 3. 接続が徐々に蓄積されていくことを確認
 4. 最終的に「database is locked」や接続エラーが発生する

## その他の情報 (Other information):
**該当コード箇所:**
`app/repositories/spot_repository.py` 76-98行目付近

```python
def update_rating(self, spot_id, avg_rating, review_count):
    """観光地の評価を更新"""
    conn = get_db()

    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tourist_spots
            SET avg_rating = ?, review_count = ?
            WHERE spot_id = ?
        ''', (avg_rating, review_count, spot_id))

        conn.commit()

        return {'success': True, 'message': '評価を更新しました'}
    except Exception as e:
        conn.rollback()
        print(f"観光地評価の更新エラー: {e}")
        return {'success': False, 'error': str(e)}
    # データベース接続を閉じる処理が実装されていない
```

**ヒント:**
- `finally`句を追加して、成功・失敗に関わらず必ずデータベース接続を閉じる必要があります
- `finally`句は、tryブロックの成功・失敗に関わらず必ず実行されます
- `close_db(conn)` を呼び出して接続を解放しましょう
- Pythonの`with`文を使うと、自動的にリソースを解放できます:
  ```python
  with get_db() as conn:
      cursor = conn.cursor()
      # ...処理...
  # with文を抜けると自動的にclose()が呼ばれる
  ```

**参考URL:**
- https://docs.python.org/ja/3/library/sqlite3.html#using-the-connection-as-a-context-manager

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_5/C`

**PRタイトル例:**
```
[Level 5-C] 問題の簡単な説明
```
