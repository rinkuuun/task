# このリポジトリについて

くじらのゼロ賃貸（株式会社クラッシハウス）のブログ記事リライト作業用。

- ブログ記事（HTML・テキスト・URL）が送られてきたら、指示がなくても `kujira-aio-rewrite` スキルで処理する（`/kujira-aio-rewrite` でも呼び出せる）。
- 成果物は `rewrites/<記事タイトル>/` に保存し、`check_output.py` の ERROR が0件になってから納品・コミットする。
