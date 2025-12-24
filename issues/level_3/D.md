<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
/spot-detail.html

## 問題の簡単な説明 (Explain the problem):
レビュー投稿フォームで、JavaScriptによる星評価のバリデーション（入力値チェック）が実装されていません。現在はHTMLの`required`属性（必須入力を設定する記述）とデータベースのCHECK制約（データの条件を制限する仕組み）で守られていますが、JavaScriptでも適切にチェックされるべきです。

## どうあるべきか (To be):
 - JavaScriptで星評価が選択されているかチェックし、分かりやすいエラーメッセージを表示すべきです。
 - HTMLやデータベースだけに頼らず、フロントエンド側でもユーザーに適切なフィードバックを提供する必要があります。
 - 必ず1〜5個の星を選択してから投稿できるようにする必要があります。

## 再現する手順 (Steps to reproduce the problem):
 1. `frontend/spot-detail.js` 243-247行目を確認する
 2. 星評価0のチェック処理が実装されていないことを確認する
 3. （検証用）HTMLの`spot-detail.html` 398行目の`required`属性を一時的に削除すると、星評価なしで送信できてしまう（データベースでエラーになる）
 4. JavaScriptでのバリデーションが機能していないことを確認

## その他の情報 (Other information):
**該当コード箇所:**
`frontend/spot-detail.js` 243-247行目付近

```javascript
async function submitReview(event) {
    event.preventDefault();
    // ...
    const rating = document.getElementById('ratingValue').value;
    const text = document.getElementById('reviewText').value;

    // ここに星評価0のチェック処理が必要
}
```

**ヒント:**
- 星評価が0の場合はアラート（警告メッセージ）を表示して、処理を中断する必要があります
- `if (rating === '0')` で判定できます
- アラートを表示した後、`return`（処理を終了する命令）で処理を中断しましょう
- 多層防御（HTMLバリデーション、JavaScriptバリデーション、データベース制約）の考え方を学びましょう

**参考情報:**
- 現在の防御層（チェックの仕組み）:
  - HTML: `<input required>` 属性（398行目）
  - JavaScript: 実装されていない（243-247行目）← **修正対象**
  - Database: `CHECK(rating >= 1 AND rating <= 5)` 制約（init_db.py 81行目）

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_3/D`

**PRタイトル例:**
```
[Level 3-D] 問題の簡単な説明
```
