<!--
**姿勢 Attitude**
- より**具体的**に、明示する。Explain the issue **concretely**.
- **否定的**な言葉を使わなくても説明はできる。Explain the issue without **negative** sentence.
- 情報に**URL**があるならば書く。Write **URL** which indicates the information.
- 説明するよりも、**図示する**。**Image** is better than text.
 -->

## 画面・API (Page or API):
POST /api/reviews (画像アップロード)

## 問題の簡単な説明 (Explain the problem):
画像アップロード機能に、ファイル拡張子偽装対策が不足しています。悪意のあるユーザーが`.php`ファイルを`.jpg`にリネームすることで、サーバーに実行可能なスクリプトをアップロードできる可能性があります。

## どうあるべきか (To be):
 - ファイルの実際の種別（MIMEタイプやマジックナンバー）を検証する必要があります。
 - 拡張子だけでなく、ファイルの内容をチェックしてから保存するべきです。

## 再現する手順 (Steps to reproduce the problem):
 1. テキストエディタで以下の内容のファイルを作成:
    ```php
    <?php phpinfo(); ?>
    ```
 2. ファイル名を `test.jpg` として保存する
 3. ブラウザで `/spot-detail.html?id=1` にアクセスする
 4. ログインして、上記の`test.jpg`をレビューに添付して投稿する
 5. 画像が正常にアップロードされることを確認
 6. アップロードされたファイルはPHPコードを含んでいるが、拡張子チェックのみで通過している

## その他の情報 (Other information):
**該当コード箇所:**
`app/services/file_service.py` 15-21行目付近

```python
def save_review_photo(self, file, review_id):
    try:
        # ファイル拡張子偽装対策不足
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in Config.ALLOWED_EXTENSIONS:
            return 'jpg, jpeg, png, gifのみ対応しています'

        # ファイルを保存
        filename = f'review_{review_id}_{uuid.uuid4().hex[:8]}{file_ext}'
        # ...
```

**ヒント:**

### 問題の本質
現在のコードは**ファイル名の拡張子だけ**をチェックしています。しかし、ファイル名は簡単に変更できるため、悪意のあるファイル（スクリプトファイルなど）を画像ファイルの拡張子（.jpg など）に偽装することができてしまいます。

### 解決方法
ファイルの**実際の内容（マジックナンバー）** をチェックする必要があります。

**マジックナンバーとは？**
ファイルの先頭数バイトに書かれている、そのファイルの種類を示す固有のバイト列（データのパターン）です。例えば：
- JPEG画像: `FF D8 FF` で始まる
- PNG画像: `89 50 4E 47` で始まる
- GIF画像: `47 49 46 38` で始まる

拡張子を変更しても、このマジックナンバーは変わらないため、本当の画像ファイルかどうかを判定できます。

### 実装方法

**方法1: `imghdr`モジュールを使う（推奨）**

Pythonの標準ライブラリ`imghdr`を使うと、ファイルの内容を読み取って実際の画像形式を判定できます。

```python
import imghdr

def save_review_photo(self, file, review_id):
    try:
        # ファイルの内容を一時的に読み取る
        file_data = file.read()

        # ファイルの実際の形式を判定（マジックナンバーをチェック）
        file_type = imghdr.what(None, file_data)

        # 画像形式でない、または許可されていない形式の場合はエラー
        if file_type not in ['jpeg', 'png', 'gif']:
            return '画像ファイルではありません'

        # ファイルポインタを先頭に戻す（後で保存するため）
        file.seek(0)

        # 拡張子もチェック（念のため）
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in Config.ALLOWED_EXTENSIONS:
            return 'jpg, jpeg, png, gifのみ対応しています'

        # ファイルを保存
        filename = f'review_{review_id}_{uuid.uuid4().hex[:8]}{file_ext}'
        # ...
```

**方法2: MIMEタイプをチェックする**

ブラウザが送信するMIMEタイプ（ファイルの種類を示す情報）をチェックする方法もありますが、これは**クライアント側で偽装可能**なため、単独では不十分です。`imghdr`と併用することをおすすめします。

```python
# MIMEタイプのチェック（補助的に使用）
if file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
    return '不正なファイル形式です'
```

**方法3: `PIL/Pillow`ライブラリを使う**

より厳密にチェックしたい場合は、実際に画像として開けるかを試すこともできます。

```python
from PIL import Image

try:
    # 画像として開けるか試す
    img = Image.open(file)
    img.verify()  # 画像ファイルとして正しいか検証

    # 許可された形式かチェック
    if img.format.lower() not in ['jpeg', 'png', 'gif']:
        return '対応していない画像形式です'
except Exception:
    return '画像ファイルではありません'
```

### セキュリティのベストプラクティス
1. **多層防御**: 拡張子チェック + マジックナンバーチェック の両方を実施
2. **ファイルサイズ制限**: 大きすぎるファイルは拒否
3. **ファイル名のサニタイズ**: 危険な文字を除去
4. **保存場所の分離**: アップロードされたファイルは実行されない場所に保存

**参考URL:**
- https://docs.python.org/ja/3/library/imghdr.html
- https://pillow.readthedocs.io/
- https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload

---

## プルリクエスト (Pull Request):

修正が完了したら、プルリクエストを作成してください。

**必須ラベル:**
- `level_5/B`

**PRタイトル例:**
```
[Level 5-B] 問題の簡単な説明
```
