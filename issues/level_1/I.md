<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
/promotion.html

## 問題の簡単な説明 (Explain the problem):
ヒーローセクション（メイン画像とタイトルのエリア）の「今すぐ観光地を探す」ボタンをクリックすると、404エラーが表示されます。

## どうあるべきか (To be):
 - ボタンをクリックすると観光地一覧ページ（spots.html）に切り替わるべきです。
 - リンク先のファイル名が正しく設定されている必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. ブラウザで `/promotion.html` にアクセスする
 2. ページ上部のヒーローセクションにある「今すぐ観光地を探す」ボタンをクリックする
 3. 404エラー（ページが見つかりません）が表示されることを確認

## その他の情報 (Other information):
**該当コード箇所:**
`frontend/promotion.html` 205行目付近

```html
<a href="spot.html" class="cta-button">今すぐ観光地を探す</a>
<!-- ↑ リンク先のファイル名を確認しましょう -->
```

**ヒント:**
- リンク先が `spot.html` になっていますが、実際のファイル名は `spots.html`（複数形）です
- HTMLの `href` 属性（リンク先の指定）の値を修正しましょう
- `frontend/` フォルダ内にどのファイルが存在するか確認してみましょう

**現在の画面:**
<img src="./images/I_1.png" />

**正しいデザイン:**
<img src="./images/I_2.png" />

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_1/I`

**PRタイトル例:**
```
[Level 1-I] 問題の簡単な説明
```
