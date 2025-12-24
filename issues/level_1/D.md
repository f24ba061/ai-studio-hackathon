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
CTAセクション（ユーザーに行動を促すボタンエリア）の1つ目のボタンテキストに誤字があります。「観光地一欄を見る」と表示されています。

## どうあるべきか (To be):
 - 「観光地一覧を見る」と表示されるべきです。
 - 正しい漢字表記である必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. ブラウザで `/promotion.html` にアクセスする
 2. 「さあ、群馬の旅を始めよう！」セクションまでスクロールする
 3. 1つ目のボタン（赤いボタン）のテキストを確認する
 4. 「観光地一欄を見る」と表示されていることを確認

## その他の情報 (Other information):
**該当コード箇所:**
`frontend/promotion.html` 261行目付近

```html
<a href="spots.html" class="cta-button">観光地一欄を見る</a>
<!-- ↑ 「欄」を「覧」に修正しましょう -->
```

**ヒント:**
- 「一覧」が正しい表記です
- リストを意味する場合は「覧」を使います

**現在の画面:**
<img src="./images/D_1.png" />

**正しいデザイン:**
<img src="./images/D_2.png" />

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_1/D`

**PRタイトル例:**
```
[Level 1-D] 問題の簡単な説明
```
