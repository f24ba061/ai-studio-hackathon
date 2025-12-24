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
2つ目の特徴カードのタイトルに誤字があります。「イベント上報満載」と表示されています。

## どうあるべきか (To be):
 - 「イベント情報満載」と表示されるべきです。
 - 正しい日本語表記である必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. ブラウザで `/promotion.html` にアクセスする
 2. 「群馬観光ポータルの3つの特徴」セクションまでスクロールする
 3. 2つ目のカード（🎉アイコン）のタイトルを確認する
 4. 「イベント上報満載」と表示されていることを確認

## その他の情報 (Other information):
**該当コード箇所:**
`frontend/promotion.html` 220行目付近

```html
<div class="feature-card">
    <div class="feature-icon">🎉</div>
    <h3>イベント上報満載</h3>
    <!-- ↑ 誤字を修正しましょう -->
    <p>お祭り、花火大会、季節のイベントなど、年間20件以上のイベント情報を掲載。旅行の計画に役立つタイムリーな情報をお届けします。</p>
</div>
```

**ヒント:**
- テキスト内容を確認して、正しい表記に修正しましょう

**現在の画面:**
<img src="./images/A_1.png" />

**正しいデザイン:**
<img src="./images/A_2.png" />

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_1/A`

**PRタイトル例:**
```
[Level 1-A] 問題の簡単な説明
```
