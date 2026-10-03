# MIRAIS メディアサイト

旧サイト（Wix）から移行した MIRAIS の新しいメディアサイトです。

- `index.html` … サイト本体（デザインと表示の仕組み）
- `data/articles.json` … 全記事のデータ（特集・ジャンル・タグ・本文）
- `images/` … 記事の写真（旧サイトから自動で取り込み）
- `scripts/fetch_images.py` と `.github/workflows/fetch-images.yml` … 写真を自動で取り込む仕組み

記事の追加や修正は、Claude に頼めば `data/articles.json` を更新して反映します。
