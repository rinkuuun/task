# くじらのゼロ賃貸（株式会社クラッシハウス） ブログ記事 AIOリライトプロンプト

以下のブログ記事を、①内容チェックと修正 → ②AIO（Google AI Overview）対策に最適化したHTMLへのリライト の順で処理してください。

このサイトの対策方針：名古屋市の全区で「〇〇区 賃貸 仲介手数料無料」の検索・AI回答に表示されることを目指す。記事内では、名古屋市の区名と「仲介手数料無料（0円）」の賃貸探しを自然に結びつけて書く。

---

## ■ 最重要：本文にコードが表示されないHTMLにする

本文HTMLはCMSのブログ本文にそのまま貼り付けて使う。CMSのエディタは `<style>` などのタグを削除したり、中身（CSS）を文字として表示したりするため、**記事の上部や途中にコードが丸見えになる**。これを防ぐため、以下を必ず守る。

### 使ってはいけないもの（本文HTMLに一切入れない）
- `<style>` タグ・CSSのまとまり（`.xxx { … }` の形の記述）→ 装飾はすべて各タグの `style="…"` 属性で指定する
- `class` 属性・`id` 属性に頼った装飾（`class` は付けない。`id` はFAQのアンカーリンク先の見出しにだけ付ける）
- `<!DOCTYPE html>`、`<html>`、`<head>`、`<body>`、`<meta>`、`<title>`、`<link>` タグ
- `<script>` タグ（構造化データ JSON-LD を含む）→ 下記「出力形式」の②に分けて出力する
- `<svg>`、`<iframe>`、`<form>`、`<input>`、`<button>` タグ（CMSに消されるか、コードとして表示される）
- `<section>`、`<header>`、`<footer>`、`<nav>`、`<aside>`、`<time>` タグ（CMSに消されると装飾が崩れる）→ `<div>` と `<span>` で代用する
- HTMLコメント（`<!-- -->`）→ 修正レポート・meta description案は③としてチャットに書く
- Markdownのコード記号（```html など）、「以下がHTMLです」などの説明文

### 書き方のルール
- 使ってよいタグ：`<div>` `<p>` `<h2>` `<h3>` `<h4>` `<span>` `<strong>` `<a>` `<ul>` `<ol>` `<li>` `<dl>` `<dt>` `<dd>` `<br>`
- 本文HTMLは必ず `<div style="…">`（記事全体を囲む外枠）で始まり、その `</div>` で終わること。その前後に1文字も入れない
- **空行を入れない**（CMSが空行を余白や `<br>` に変換するため）。インデント（字下げ）もしない
- `style` 属性の値はダブルクォート `"` で囲み、中でダブルクォートを使わない（フォント名などが必要ならシングルクォート）
- 1つの `style` 属性の中に改行を入れない
- `:hover` や `@media`（レスポンシブ指定）は `style` 属性では書けないため使わない。代わりに下記「装飾スタイル」の `max-width:100%`・`box-sizing:border-box`・`flex-wrap:wrap` でスマホ幅に自動で収まるようにする

---

## ■ STEP1：元記事の内容チェックと修正（リライト前に必ず実施）

元記事を読み、以下の観点で問題がないか確認し、問題があれば修正したうえでリライトする。

### チェック項目
1. **事実の誤り**：賃貸借契約・仲介手数料・敷金礼金・原状回復・更新料・保証会社・入居審査など、賃貸取引や法律に関する説明の誤り
2. **古い情報**：法改正・ガイドライン・補助金・相場など、年によって変わる情報が現在の制度と合っているか。記事中の「〇年まで」「現在は」などの期限・時点表現
3. **地域情報の誤り**：名古屋市の区名・エリア区分・駅名・路線名などの誤り、他地域の情報の混入
4. **記事内の矛盾**：本文とFAQ、見出しと本文で内容・数値が食い違っていないか
5. **不適切な表現**：「絶対」「完全」「最高」「最安」「日本一」「業界一」「名古屋で一番」「格安」「激安」「掘出物」など、不動産の表示に関する公正競争規約で使用が制限される用語や、根拠のない断定・誇大表現
6. **他社情報の残骸**：くじらのゼロ賃貸（株式会社クラッシハウス）以外の社名・電話番号・URL・エリアが残っていないか
7. **誤字脱字・不自然な日本語**

### 修正のルール
- 確信を持って正しいと言える場合のみ修正する。**確信がない箇所は修正せず【要確認】として報告する**
- 年によって変わる制度・数値は、ウェブ検索が使える場合は公的機関（国土交通省・消費者庁・名古屋市など）の情報で確認する。確認できない場合は【要確認】に回す
- 根拠のない数値を新たに作らない（下記「数値の具体化」も同様）
- **仲介手数料0円の書き方**：一部対象外の物件があるため、「仲介手数料0円（無料）」と書くときは、記事内で最初に出てくる箇所と、まとめの会社紹介に「※一部対象外の物件があります」を必ず添える。「全物件」「どの物件でも必ず」など、すべての物件が無料と読める書き方はしない

### 修正レポート
本文HTMLには入れず、出力形式の③としてチャットに以下の形で書く。

```
【修正レポート】
・修正1：（修正前）→（修正後）／理由：
・修正2：…
【要確認】
・（該当箇所）／確認してほしい点：
```
問題がなかった場合は「修正なし」と記載する。

---

## ■ STEP2：AIO対策の方針

### 1. 構造化データ（JSON-LD）は本文と分けて出力する
`<script type="application/ld+json">` で以下4種類を含め、**本文HTMLとは別の②として出力する**（本文HTMLには入れない）。
- **FAQPage**：FAQ目次の4つのQ&Aを`mainEntity`に対応。Q＝`Question.name`、A＝`acceptedAnswer.text`（本文と矛盾しない40〜80文字の要約で、結論を明示）
- **Article**：`headline`、`author`（Person：背古 涼介、url：https://www.kujira-zerochintai.com/staff/253354/）、`publisher`（Organization：くじらのゼロ賃貸 株式会社クラッシハウス、ロゴURL：https://hp-asp-lab5.s3.ap-northeast-1.amazonaws.com/kujira-zerochintai.com/logo/logo.png）。**`datePublished`・`dateModified` は入れない**（投稿日はCMSで設定するため）
- **BreadcrumbList**：トップ（https://www.kujira-zerochintai.com/）＞ブログ（https://www.kujira-zerochintai.com/blog/）＞カテゴリ＞記事タイトル
- **LocalBusiness（RealEstateAgent）**：店舗名（くじらのゼロ賃貸 株式会社クラッシハウス）、url（https://www.kujira-zerochintai.com/）、住所（〒485-0068 愛知県小牧市藤島１丁目239番地）、電話番号（0568-70-3096）、営業時間（10:00〜19:00、水曜定休）、営業エリア（areaServed：名古屋市）。`aggregateRating`は含めない

### 2. AIが抽出しやすい文章構造
- **結論ファースト**：各H3直後の1文目で結論を言い切る（「〜は可能です。理由は〜」の順）
- **数値の具体化**：「安い」「早い」などの曖昧な表現は、元記事や公的情報など**根拠のある数値がある場合のみ**定量化する。根拠のない数値を作るくらいなら、曖昧表現を避けた具体的な言い回しにする
- **要約ボックス**：導入文とFAQ目次の間に3行程度の「この記事でわかること」
- **見出し構造**：H2→H3の階層を崩さない。各H2には `id` 属性（例：`id="sec1"`）を付け、FAQ目次からリンクする
- **エリア名の入れ方**：記事のテーマに関係する名古屋市の区名を、導入文・見出し・FAQに自然に入れる（キーワードの詰め込みはしない）

### 3. E-E-A-Tの明示
- 監修者情報ブロック：「監修：背古 涼介（代表取締役／不動産キャリア7年）」と、プロフィールページ（https://www.kujira-zerochintai.com/staff/253354/）へのリンクのみ。資格は書かない。このブロックの下に個別の問い合わせリンクは置かない
- 実績：宅地建物取引業免許 愛知県知事（1）第26010号／全日本不動産協会 愛知県本部 加盟

### 4. 内部リンクのアンカーテキスト
「こちら」ではなく「名古屋市中区の仲介手数料無料の賃貸を探す」のように、区名を入れた具体的な名詞句にする

### 5. 日付の扱い
- 投稿日・公開日・更新日は、本文にも構造化データにも一切書かない（いえらぶCLOUDの管理画面で設定する）
- 本文中で「〇年〇月現在」など時点を示す必要がある場合は、元記事に書かれている時点表現をチェック項目2で確認したうえで使う

### 6. メタ情報
`<meta name="description">`案（120文字程度、結論と名古屋市の区名を含む）を1つ、出力形式の③に記載する（本文HTMLには入れない）

---

## ■ STEP3：HTML構成ルール

### 1. 冒頭構成
- 画像は一切使わない（アイキャッチ・セクション画像は削除）
- 外枠 `<div>` 開始 → 導入文（2〜3段落）→ 要約ボックス → FAQ目次（4つのQ&A）→ LINE・電話CTAボタン

### 2. FAQ目次
- 4つのQ&A、各セクションのH2（`id`付き）へのアンカーリンク付き
- Qの背景色・「詳細はこちらの見出しへ！▼」の色：#0B4DA2
- 各QAはFAQPageスキーマと1対1で対応

### 3. 各セクション（4セクション＋まとめ）
- H2 → 導入文 → 3ポイント要約リスト →「詳しく解説していきます！」→ H3×3
- セクション3は dl/dt/dd の枠付きブロック形式も可

### 4. セクション間CTA（各セクションの後に配置）
- お部屋探し・物件探し・初期費用の見積もり系の話題の直後 → お問い合わせ＋LINE
- どちらでもない一般的な相談 → LINEまたは電話

### 5. まとめセクション
- 振り返りリスト（4項目程度）
- くじらのゼロ賃貸の紹介文：仲介手数料0円（※一部対象外の物件があります）、SUUMO・HOME'Sなどの他社サイトやSNSで見つけた物件も紹介可能（一部対象外あり）、相見積もり歓迎、初期費用の分割相談が可能、希望の場所までの無料送迎、LINEで24時間受付、24時間内見対応、契約までオンラインで完結可能
- 監修者情報ブロック
- LINE・電話・お問い合わせ・来店予約CTAボタン

### 6. 末尾ウィジェット
- 記事末尾（外枠 `</div>` の直前）に配置。LINE・来店予約・電話・お問い合わせの4アクション
- エリアリンク（具体的なアンカーテキストで。下記「エリアリンク一覧」から記事に関係する区を中心に掲載）

### 7. 表は使わない
元記事の表（table）は、ナンバリング＋ハイライト＋リストの構成に変換する

---

## ■ 装飾スタイル（各タグの style 属性にそのまま書く）

下記の `style="…"` を、該当するタグに毎回そのまま書く（同じ種類の要素には同じ値を繰り返し書く。省略や共通化はしない）。

| 要素 | タグ | style属性の値 |
|---|---|---|
| 外枠 | div | `max-width:800px;width:100%;margin:0 auto;box-sizing:border-box;font-size:16px;line-height:1.9;color:#333;` |
| 段落 | p | `margin:0 0 1.2em;` |
| 要約ボックス | div | `background:#EBF1F8;border-left:4px solid #0B4DA2;padding:16px 20px;margin:24px 0;box-sizing:border-box;` |
| 要約ボックスの見出し | p | `font-weight:bold;color:#0B4DA2;margin:0 0 8px;` |
| FAQ目次の外枠 | div | `border:2px solid #0B4DA2;border-radius:8px;padding:16px;margin:24px 0;box-sizing:border-box;` |
| FAQのQ | p | `background:#0B4DA2;color:#fff;font-weight:bold;padding:8px 12px;border-radius:4px;margin:16px 0 8px;` |
| FAQのA | p | `margin:0 0 4px;padding-left:12px;` |
| FAQの見出しリンク | a | `color:#0B4DA2;font-weight:bold;font-size:14px;text-decoration:none;` |
| H2 | h2 | `font-size:22px;color:#333;border-bottom:3px solid #0B4DA2;padding:0 0 8px;margin:48px 0 20px;line-height:1.5;` |
| H3 | h3 | `font-size:18px;color:#fff;background:#0B4DA2;padding:10px 16px;border-radius:4px;margin:32px 0 16px;line-height:1.5;` |
| 3ポイント要約リスト | ul | `border:2px solid #0B4DA2;border-radius:8px;padding:16px 16px 16px 36px;margin:20px 0;box-sizing:border-box;` |
| ハイライト | span | `background:linear-gradient(transparent 58%,#fff000 0%);font-weight:bold;` |
| 枠付きブロック（dl） | dl | `border:2px solid #0B4DA2;border-radius:8px;padding:16px;margin:20px 0;box-sizing:border-box;` |
| 枠付きブロックの項目名（dt） | dt | `font-weight:bold;color:#0B4DA2;margin:8px 0 4px;` |
| 枠付きブロックの説明（dd） | dd | `margin:0 0 12px;` |
| 会社紹介の見出し | p | `font-size:18px;font-weight:bold;color:#0B4DA2;margin:24px 0 8px;` |
| 監修者情報ブロック | div | `border:1px solid #ddd;border-radius:8px;padding:16px;margin:24px 0;font-size:14px;box-sizing:border-box;` |
| 監修者リンク | a | `color:#0B4DA2;text-decoration:underline;` |
| 末尾ウィジェットの外枠 | div | `background:#f7f7f7;border-radius:8px;padding:20px 16px;margin:40px 0 0;box-sizing:border-box;` |
| 末尾ウィジェットの見出し | p | `font-weight:bold;text-align:center;margin:0 0 12px;` |
| エリアリンク | a | `color:#0B4DA2;text-decoration:underline;` |

---

## ■ 固定URL

- LINE：https://lin.ee/x9VvbWL
- 電話：tel:0568703096
- 来店予約：https://www.kujira-zerochintai.com/reservation/
- お問い合わせ：https://www.kujira-zerochintai.com/contact/
- 監修者プロフィール：https://www.kujira-zerochintai.com/staff/253354/
- ロゴ画像：https://hp-asp-lab5.s3.ap-northeast-1.amazonaws.com/kujira-zerochintai.com/logo/logo.png

## ■ エリアリンク一覧

アンカーテキストは「名古屋市〇〇区の仲介手数料無料の賃貸を探す」の形にする。

- 名古屋市千種区：https://www.kujira-zerochintai.com/area1c1/city_cr23101/
- 名古屋市東区：https://www.kujira-zerochintai.com/area1c1/city_cr23102/
- 名古屋市北区：https://www.kujira-zerochintai.com/area1c1/city_cr23103/
- 名古屋市西区：https://www.kujira-zerochintai.com/area1c1/city_cr23104/
- 名古屋市中村区：https://www.kujira-zerochintai.com/area1c1/city_cr23105/
- 名古屋市中区：https://www.kujira-zerochintai.com/area1c1/city_cr23106/
- 名古屋市昭和区：https://www.kujira-zerochintai.com/area1c1/city_cr23107/
- 名古屋市瑞穂区：https://www.kujira-zerochintai.com/area1c1/city_cr23108/
- 名古屋市熱田区：https://www.kujira-zerochintai.com/area1c1/city_cr23109/
- 名古屋市中川区：https://www.kujira-zerochintai.com/area1c1/city_cr23110/
- 名古屋市港区：https://www.kujira-zerochintai.com/area1c1/city_cr23111/
- 名古屋市守山区：https://www.kujira-zerochintai.com/area1c1/city_cr23113/
- 名古屋市緑区：https://www.kujira-zerochintai.com/area1c1/city_cr23114/
- 名古屋市名東区：https://www.kujira-zerochintai.com/area1c1/city_cr23115/
- 名古屋市天白区：https://www.kujira-zerochintai.com/area1c1/city_cr23116/

※ 名古屋市南区は物件検索ページがないため、リンクを作らない（南区の話題は本文で扱ってよいが、URLを作らない）

---

## ■ 導線カラー（ボタン等の行動喚起要素にのみ使用）

| 導線 | グラデーション（style属性の background に書く値） | 使用箇所 |
|---|---|---|
| LINE | `linear-gradient(135deg,#06C755,#05b34c)` | 冒頭・途中・まとめ・末尾 |
| 電話 | `linear-gradient(135deg,#0B4DA2,#09418A)` | 冒頭・途中・まとめ・末尾 |
| お問い合わせ | `linear-gradient(135deg,#6c5ce7,#5849c2)` | 途中（お部屋探し系の直後）・まとめ・末尾 |
| 来店予約 | `linear-gradient(135deg,#2a9d8f,#22857a)` | まとめ・末尾のみ |

- 見出し・FAQ・枠などの装飾はブランドカラー（#0B4DA2）で統一し、導線カラーと混同しない
- ボタンの文字色は `color:#fff !important;text-decoration:none !important;` を必ず書く（CMSのリンク色に上書きされないため）

---

## ■ CTAボタンHTML（この形のまま使う。空行・インデントを入れない）

ボタンを並べる外枠：
`<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:28px 0;">`

ボタン1つの共通style（background の値だけ導線ごとに差し替える）：
`display:block;flex:1 1 240px;max-width:100%;box-sizing:border-box;padding:16px 12px;border-radius:50px;text-align:center;font-size:16px;font-weight:bold;line-height:1.4;color:#fff !important;text-decoration:none !important;box-shadow:0 3px 8px rgba(0,0,0,0.15);background:（導線カラー）;`

### LINE・電話（冒頭とまとめ）
```html
<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:28px 0;">
<a href="https://lin.ee/x9VvbWL" target="_blank" rel="nofollow" style="display:block;flex:1 1 240px;max-width:100%;box-sizing:border-box;padding:16px 12px;border-radius:50px;text-align:center;font-size:16px;font-weight:bold;line-height:1.4;color:#fff !important;text-decoration:none !important;box-shadow:0 3px 8px rgba(0,0,0,0.15);background:linear-gradient(135deg,#06C755,#05b34c);">LINEで相談する</a>
<a href="tel:0568703096" style="display:block;flex:1 1 240px;max-width:100%;box-sizing:border-box;padding:16px 12px;border-radius:50px;text-align:center;font-size:16px;font-weight:bold;line-height:1.4;color:#fff !important;text-decoration:none !important;box-shadow:0 3px 8px rgba(0,0,0,0.15);background:linear-gradient(135deg,#0B4DA2,#09418A);">電話で相談する（0568-70-3096）</a>
</div>
```

### お部屋探し系（お部屋探し・物件探し・初期費用系セクションの直後。お問い合わせ＋LINE）
```html
<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:28px 0;">
<a href="https://www.kujira-zerochintai.com/contact/" style="display:block;flex:1 1 240px;max-width:100%;box-sizing:border-box;padding:16px 12px;border-radius:50px;text-align:center;font-size:16px;font-weight:bold;line-height:1.4;color:#fff !important;text-decoration:none !important;box-shadow:0 3px 8px rgba(0,0,0,0.15);background:linear-gradient(135deg,#6c5ce7,#5849c2);">お問い合わせはこちら</a>
<a href="https://lin.ee/x9VvbWL" target="_blank" rel="nofollow" style="display:block;flex:1 1 240px;max-width:100%;box-sizing:border-box;padding:16px 12px;border-radius:50px;text-align:center;font-size:16px;font-weight:bold;line-height:1.4;color:#fff !important;text-decoration:none !important;box-shadow:0 3px 8px rgba(0,0,0,0.15);background:linear-gradient(135deg,#06C755,#05b34c);">LINEで相談する</a>
</div>
```

### お問い合わせ・来店予約（まとめ・末尾ウィジェット）
```html
<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:28px 0;">
<a href="https://www.kujira-zerochintai.com/contact/" style="display:block;flex:1 1 240px;max-width:100%;box-sizing:border-box;padding:16px 12px;border-radius:50px;text-align:center;font-size:16px;font-weight:bold;line-height:1.4;color:#fff !important;text-decoration:none !important;box-shadow:0 3px 8px rgba(0,0,0,0.15);background:linear-gradient(135deg,#6c5ce7,#5849c2);">お問い合わせはこちら</a>
<a href="https://www.kujira-zerochintai.com/reservation/" style="display:block;flex:1 1 240px;max-width:100%;box-sizing:border-box;padding:16px 12px;border-radius:50px;text-align:center;font-size:16px;font-weight:bold;line-height:1.4;color:#fff !important;text-decoration:none !important;box-shadow:0 3px 8px rgba(0,0,0,0.15);background:linear-gradient(135deg,#2a9d8f,#22857a);">来店予約はこちら</a>
</div>
```

※ 上の ```html の記号はこのプロンプト内で見本を示すためのもの。出力する本文HTMLには ``` を入れない。

---

## ■ 出力形式

以下の3つに分けて出力する。

**① 本文HTML（CMSのブログ本文に貼る用）**
- ダウンロード可能なファイル「記事タイトル_本文.html」として出力
- 中身は記事全体を囲む外枠 `<div style="…">…</div>` だけ。先頭は `<div style=`、末尾は `</div>`
- `<style>`・`class=`・`<svg`・`<!DOCTYPE>`・`<html>`・`<head>`・`<body>`・`<meta>`・`<title>`・`<script>`・HTMLコメント・説明文・投稿日は入れない
- 空行・インデントを入れない

**② 構造化データ（JSON-LD）**
- ダウンロード可能なファイル「記事タイトル_構造化データ.html」として出力
- 中身は `<script type="application/ld+json">…</script>` だけ
- 「CMSのheadタグ・SEO用コード挿入欄に貼ってください。挿入欄がない場合、本文には貼らないでください」と一言添える

**③ チャットでの報告**
- 修正レポート（修正内容・【要確認】）
- meta description案（120文字程度）
- 「本文HTMLは、CMSエディタをHTML（ソース）編集モードにしてから貼り付けてください。投稿日はいえらぶCLOUDの管理画面で設定してください」と一言添える

### 出力前チェック
①を出す前に、以下を自分で確認し、当てはまるものがあれば取り除いてから出力する。
- 1行目が `<div style=` で始まっているか（その前に `<style`・`<!DOCTYPE`・`<html`・`<head`・`<meta`・`<script`・`<!--`・``` ・説明文がないか）
- 本文中に `<style`・`</style>`・`{`・`}`・`class=`・`<svg`・`<script`・`<!--`・``` が1つも残っていないか
- 空行が1つもないか
- 最終行が外枠の `</div>` で終わっているか（開始タグと終了タグの数が合っているか）
- 公開日・更新日などの日付表示が入っていないか
- 「仲介手数料0円（無料）」の初出とまとめに「一部対象外の物件があります」が添えられているか
- 「最安」「名古屋で一番」など、チェック項目5の用語が残っていないか
