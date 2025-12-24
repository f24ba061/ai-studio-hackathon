<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
/spots.html

## 問題の簡単な説明 (Explain the problem):
人気ランキングに表示される星評価の数が正しくありません。例えば、平均評価が4.5の観光地に対して、星が6個表示されることがあります。

## どうあるべきか (To be):
 - 平均評価4.5の場合、満点の星4個 + 半星1個 = 合計5個以内で表示されるべきです。
 - 星の総数は常に5個以内である必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. ブラウザで `/spots.html` にアクセスする
 2. ページ右側の「人気ランキング」セクションを確認する
 3. 各観光地の星評価を数える
 4. 星の総数が5個を超えている観光地があることを確認

## その他の情報 (Other information):
**該当コード箇所:**
`frontend/spots.js` 169行目付近

```javascript
// ランキング内の星評価表示
const fullStars = Math.ceil(spot.avg_rating);  // ← ここに問題があります
const hasHalfStar = spot.avg_rating % 1 >= 0.5;
const emptyStars = 5 - fullStars;
const starsHtml = '★'.repeat(fullStars) + (hasHalfStar ? '☆' : '') + '☆'.repeat(emptyStars);
```

**ヒント:**
- `Math.ceil()` は小数点を切り上げる関数（処理）です（例: 4.3 → 5）
- `Math.floor()` は小数点を切り捨てる関数です（例: 4.3 → 4）
- 星の計算ロジック（処理の流れ）を見直してみましょう

**現在の画面:**
<img src="./images/E_1.png" />

**正しいデザイン:**
<img src="./images/E_2.png" />

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_2/E`

**PRタイトル例:**
```
[Level 2-E] 問題の簡単な説明
```
