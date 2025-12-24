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
レビューに添付された画像をクリックして拡大表示したとき、ESCキーを押してもモーダル（画面上に重ねて表示されるウィンドウ）が閉じません。

## どうあるべきか (To be):
 - 画像拡大モーダルを表示中にESCキーを押すと、モーダルが閉じるべきです。
 - これは一般的なUIの動作パターンです。

## 再現する手順 (Steps to reproduce the problem):
 1. ブラウザで `/spot-detail.html?id=1` にアクセスする
 2. ログインする（ユーザーID: 4, パスワード: password789）
 3. レビューを投稿する際に、画像を添付する
 4. 投稿後、添付した画像をクリックして拡大表示する
 5. ESCキーを押す
 6. モーダルが閉じないことを確認（画面をクリックすると閉じる）

## その他の情報 (Other information):
**該当コード箇所:**
`frontend/spot-detail.js` 378-383行目付近

**問題点:**
- ESCキーでモーダルを閉じる処理が実装されていません
- 現在はモーダルの背景をクリックすることでしか閉じられません

**ヒント:**
- `document.addEventListener('keydown', ...)` でキーボードイベント（キー入力の動作）を監視できます
- イベントオブジェクト（イベント情報を持つデータ）の `e.key === 'Escape'` でESCキーを判定できます
- ESCキーが押されたときに `closeImageModal()` を呼び出す（実行する）ようにしましょう

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_2/J`

**PRタイトル例:**
```
[Level 2-J] 問題の簡単な説明
```
