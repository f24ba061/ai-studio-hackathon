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
レビュー投稿フォームで、JavaScriptによるレビュー内容のバリデーション（入力値チェック）が実装されていません。現在はHTMLの`required`属性（必須入力を設定する記述）で空欄チェックされていますが、空白スペースのみの入力は弾けません。

## どうあるべきか (To be):
 - JavaScriptでレビュー内容が空白または空白スペースのみの場合、エラーメッセージを表示すべきです。
 - `.trim()`メソッド（文字列の前後の空白を削除する機能）を使って、前後の空白を除去した上でチェックする必要があります。
 - HTMLの`required`属性だけでなく、JavaScriptでも適切にバリデーションすべきです。

※メソッド: オブジェクトに用意されている機能

## 再現する手順 (Steps to reproduce the problem):
 1. `frontend/spot-detail.js` 249-253行目を確認する
 2. レビュー内容の空チェック処理が実装されていないことを確認する
 3. （検証用）HTMLの`spot-detail.html` 404行目の`required`属性を一時的に削除すると、空白スペースのみでも送信できてしまう
 4. JavaScriptでのバリデーションが機能していないことを確認

## その他の情報 (Other information):
**該当コード箇所:**
`frontend/spot-detail.js` 249-253行目付近

```javascript
async function submitReview(event) {
    event.preventDefault();
    // ...
    const rating = document.getElementById('ratingValue').value;
    const text = document.getElementById('reviewText').value;

    // ここにレビュー内容の空チェック処理が必要
    // text.trim() で前後の空白を除去してチェック
}
```

**ヒント:**
- `.trim()`メソッドは、文字列の前後の空白を削除します（例: `"  hello  ".trim()` → `"hello"`）
- `if (!text.trim())` で、空文字列または空白のみの文字列を判定できます
- 空の場合はアラート（警告メッセージ）を表示して、`return`（処理を終了する命令）で処理を中断しましょう
- D.mdの星評価バリデーションと同様の多層防御の考え方が適用できます

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_3/E`

**PRタイトル例:**
```
[Level 3-E] 問題の簡単な説明
```
