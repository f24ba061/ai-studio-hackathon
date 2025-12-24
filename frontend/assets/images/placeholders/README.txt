プレースホルダー画像フォルダ
========================

このフォルダには、画像が見つからない場合の代替画像を配置します。

推奨ファイル:
- no-image.jpg: 観光地画像がない場合の代替画像
- loading.gif: 画像読み込み中の表示用
- error.png: 画像読み込みエラー時の表示用

使用例:
JavaScript の onerror 属性で自動的に代替画像を表示
<img src="assets/images/spots/1.jpg"
     onerror="this.src='assets/images/placeholders/no-image.jpg'">

推奨サイズ: 200x150px
形式: JPEG, PNG, GIF