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
統計ページにキャッシュ機構がなく、ページを開くたびに全てのデータを再計算しています。アクセスが多い場合、データベースに大きな負荷がかかり、ページの読み込みが遅くなります。

## どうあるべきか (To be):
 - 統計データは一定時間キャッシュされ、頻繁な再計算を避けるべきです。
 - キャッシュの有効期限を設定し、適切なタイミングで更新される必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. ブラウザで `/stats.html` に複数回アクセスする
 2. ブラウザの開発者ツールのネットワークタブで、毎回APIが呼ばれていることを確認
 3. サーバーのログで、毎回データベースクエリが実行されていることを確認
 4. データ量が多い場合、読み込みが遅いことを体感する

## その他の情報 (Other information):
**該当コード箇所:**
`app/services/stats_service.py` 6-7行目付近

```python
class StatsService:
    def __init__(self):
        self.stats_repo = StatsRepository()
        # キャッシュ機構がないため、ページアクセス毎に全データを取得して遅い
        # 修正方法: flask-cachingを使うか、簡易的なメモリキャッシュを実装する

    def get_summary(self):
        summary = self.stats_repo.fetch_summary()
        # ...毎回データベースから取得...
```

**ヒント:**
- Flaskの`flask-caching`ライブラリを使うと簡単にキャッシュ（一度取得したデータを一時的に保存して再利用する仕組み）を実装できます
- 例:
  ```python
  from flask_caching import Cache

  cache = Cache(app, config={'CACHE_TYPE': 'simple'})

  @cache.cached(timeout=300)  # 5分間キャッシュ
  def get_summary(self):
      return self.stats_repo.fetch_summary()
  ```
- または、簡易的なメモリキャッシュを実装する方法:
  ```python
  import time

  class StatsService:
      def __init__(self):
          self.cache = {}
          self.cache_timeout = 300  # 5分

      def get_summary(self):
          now = time.time()
          if 'summary' in self.cache:
              cached_data, cached_time = self.cache['summary']
              if now - cached_time < self.cache_timeout:
                  return cached_data

          # キャッシュがない、または期限切れの場合のみデータ取得
          summary = self.stats_repo.fetch_summary()
          self.cache['summary'] = (summary, now)
          return summary
  ```

**参考URL:**
- https://flask-caching.readthedocs.io/

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_5/F`

**PRタイトル例:**
```
[Level 5-F] 問題の簡単な説明
```
