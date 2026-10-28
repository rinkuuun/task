#!/usr/bin/env python3
"""くじらのゼロ賃貸 AIOリライトの出力チェック。

使い方:
    python3 check_output.py rewrites/<記事タイトル>
    python3 check_output.py <本文.html> [<構造化データ.html>]

フォルダを渡すと *_本文.html と *_構造化データ.html を探して両方チェックする。
ERROR が1件でもあれば終了コード1。
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ALLOWED_TAGS = {"div", "p", "h2", "h3", "h4", "span", "strong", "a", "ul", "ol",
                "li", "dl", "dt", "dd", "br"}
VOID_TAGS = {"br", "img", "hr", "meta", "link", "input"}

OUTER_STYLE = ("max-width:800px;width:100%;margin:0 auto;box-sizing:border-box;"
               "font-size:16px;line-height:1.9;color:#333;")
H2_STYLE = ("font-size:22px;color:#333;border-bottom:3px solid #0B4DA2;padding:0 0 8px;"
            "margin:48px 0 20px;line-height:1.5;")
H3_STYLE = ("font-size:18px;color:#fff;background:#0B4DA2;padding:10px 16px;border-radius:4px;"
            "margin:32px 0 16px;line-height:1.5;")
FAQ_Q_STYLE = ("background:#0B4DA2;color:#fff;font-weight:bold;padding:8px 12px;"
               "border-radius:4px;margin:16px 0 8px;")
BTN_COMMON = ("display:block;flex:1 1 240px;max-width:100%;box-sizing:border-box;padding:16px 12px;"
              "border-radius:50px;text-align:center;font-size:16px;font-weight:bold;line-height:1.4;"
              "color:#fff !important;text-decoration:none !important;"
              "box-shadow:0 3px 8px rgba(0,0,0,0.15);background:")

SITE = "https://www.kujira-zerochintai.com/"
FIXED_URLS = {
    "https://lin.ee/x9VvbWL": "linear-gradient(135deg,#06C755,#05b34c)",
    "tel:0568703096": "linear-gradient(135deg,#0B4DA2,#09418A)",
    SITE + "contact/": "linear-gradient(135deg,#6c5ce7,#5849c2)",
    SITE + "reservation/": "linear-gradient(135deg,#2a9d8f,#22857a)",
}
STAFF_URL = SITE + "staff/253354/"
AREAS = {
    "千種区": "23101", "東区": "23102", "北区": "23103", "西区": "23104",
    "中村区": "23105", "中区": "23106", "昭和区": "23107", "瑞穂区": "23108",
    "熱田区": "23109", "中川区": "23110", "港区": "23111", "守山区": "23113",
    "緑区": "23114", "名東区": "23115", "天白区": "23116",
}
AREA_URLS = {f"{SITE}area1c1/city_cr{code}/": ku for ku, code in AREAS.items()}

BANNED_WORDS = ["絶対", "完全", "最高", "最安", "日本一", "業界一", "名古屋で一番", "格安",
                "激安", "掘出物", "掘り出し物", "全物件", "どの物件でも必ず", "No.1", "ナンバーワン"]
DISCLAIMER = "一部対象外の物件があります"
FEE_RE = re.compile(r"仲介手数料(?:が|は)?(?:0円|０円|無料|ゼロ)")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


class BodyParser(HTMLParser):
    def __init__(self, rep):
        super().__init__(convert_charrefs=True)
        self.rep = rep
        self.stack = []
        self.top_level_count = 0
        self.ids = []
        self.links = []          # (href, attrs, text)
        self._link = None
        self.h2_texts = []
        self._cur_h2 = None
        self.text_parts = []
        self.faq_q = []
        self._faq_q = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag not in ALLOWED_TAGS:
            self.rep.error(f"{line}行目: 使えないタグ <{tag}>")
        if "class" in a:
            self.rep.error(f"{line}行目: class 属性 <{tag} class=…>")
        if "id" in a:
            self.ids.append(a["id"])
            if tag != "h2":
                self.rep.error(f"{line}行目: id 属性は FAQ のリンク先 H2 にだけ付ける（<{tag} id=\"{a['id']}\">）")
        style = a.get("style")
        if style is not None and ("\n" in style or '"' in style):
            self.rep.error(f"{line}行目: style 属性内に改行またはダブルクォート")
        if not self.stack and tag not in VOID_TAGS:
            self.top_level_count += 1
            if self.top_level_count == 1 and (tag != "div" or style != OUTER_STYLE):
                self.rep.error("外枠が規定の <div style=\"" + OUTER_STYLE + "\"> になっていない")
        if tag == "h2":
            if style != H2_STYLE:
                self.rep.warn(f"{line}行目: H2 の style が規定値と違う")
            self._cur_h2 = ""
        if tag == "h3" and style != H3_STYLE:
            self.rep.warn(f"{line}行目: H3 の style が規定値と違う")
        if tag == "p" and style == FAQ_Q_STYLE:
            self._faq_q = ""
        if tag == "a":
            self._link = [a.get("href", ""), a, ""]
        if tag not in VOID_TAGS:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS and self.stack:
            self.stack.pop()

    def handle_endtag(self, tag):
        line = self.getpos()[0]
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.rep.error(f"{line}行目: 対応する開始タグのない </{tag}>")
            return
        open_tag, open_line = self.stack.pop()
        if open_tag != tag:
            self.rep.error(f"{line}行目: </{tag}> が {open_line}行目の <{open_tag}> と対応していない")
        if tag == "a" and self._link:
            self.links.append(tuple(self._link))
            self._link = None
        if tag == "h2" and self._cur_h2 is not None:
            self.h2_texts.append(self._cur_h2.strip())
            self._cur_h2 = None
        if tag == "p" and self._faq_q is not None:
            self.faq_q.append(self._faq_q.strip())
            self._faq_q = None

    def handle_data(self, data):
        self.text_parts.append(data)
        if self._link is not None:
            self._link[2] += data
        if self._cur_h2 is not None:
            self._cur_h2 += data
        if self._faq_q is not None:
            self._faq_q += data

    def handle_comment(self, data):
        self.rep.error(f"{self.getpos()[0]}行目: HTMLコメント <!-- -->")

    def handle_decl(self, decl):
        self.rep.error(f"宣言 <!{decl}> が入っている")


def check_body(path, rep):
    raw = path.read_text(encoding="utf-8")
    text = raw.lstrip("﻿")
    if raw.startswith("﻿"):
        rep.warn("先頭に BOM がある")
    if not text.startswith("<div style="):
        rep.error("1行目が <div style= で始まっていない")
    if not text.rstrip("\n").endswith("</div>"):
        rep.error("最後が </div> で終わっていない")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()  # 最終行の改行1つは許容
    for i, line in enumerate(lines, 1):
        if line.strip() == "":
            rep.error(f"{i}行目: 空行")
        elif line[0] in " \t　":
            rep.error(f"{i}行目: インデント（行頭の空白）")

    for needle, label in [("<style", "<style"), ("</style>", "</style>"), ("{", "{"), ("}", "}"),
                          ("class=", "class="), ("<svg", "<svg"), ("<script", "<script"),
                          ("<!--", "<!--"), ("```", "```"), ("<img", "<img（画像）"),
                          ("<table", "<table（表）"), ("@media", "@media"), (":hover", ":hover")]:
        n = text.count(needle)
        if n:
            rep.error(f"禁止文字列 {label} が {n} 個ある")

    p = BodyParser(rep)
    p.feed(text)
    p.close()
    for tag, line in p.stack:
        rep.error(f"{line}行目の <{tag}> が閉じられていない")
    if p.top_level_count > 1:
        rep.error("外枠 <div> の外側に要素がある（全体を1つの外枠で囲む）")

    plain = "".join(p.text_parts)

    # 日付
    for m in re.finditer(r"(公開日|投稿日|更新日|最終更新)", plain):
        rep.error(f"日付表示らしき語「{m.group(1)}」がある")
    for m in re.finditer(r"\d{4}[年/.-]\d{1,2}[月/.-]\d{1,2}日?", plain):
        rep.warn(f"日付「{m.group(0)}」がある（投稿日なら削除）")

    # 禁止用語
    for w in BANNED_WORDS:
        for m in re.finditer(re.escape(w), plain):
            ctx = plain[max(0, m.start() - 15):m.end() + 15].replace("\n", "")
            rep.warn(f"制限用語「{w}」: …{ctx}…")

    # 仲介手数料0円の注記
    fee = FEE_RE.search(plain)
    if fee:
        after = plain[fee.start():fee.start() + 120]
        if DISCLAIMER not in after:
            rep.error(f"仲介手数料0円/無料の初出（…{plain[fee.start():fee.end() + 20]}…）の近くに「※{DISCLAIMER}」がない")
    else:
        rep.warn("「仲介手数料0円/無料」の記述が見つからない")
    if plain.count(DISCLAIMER) < 2:
        rep.error(f"「※{DISCLAIMER}」が2箇所未満（初出とまとめの会社紹介に必要）")

    # 見出し・id・FAQ
    if len(p.faq_q) != 4:
        rep.error(f"FAQ目次のQ（規定 style の p）が {len(p.faq_q)} 個（4個必要）")
    ids = set(p.ids)
    if len(p.ids) != len(ids):
        rep.error("id が重複している")
    anchors = [href[1:] for href, _, _ in p.links if href.startswith("#")]
    for a in anchors:
        if a not in ids:
            rep.error(f"アンカー #{a} のリンク先 id がない")
    if len(set(anchors)) < 4:
        rep.error(f"FAQ目次から H2 へのアンカーリンクが {len(set(anchors))} 種類（4つ必要）")
    if len(p.h2_texts) < 5:
        rep.warn(f"H2 が {len(p.h2_texts)} 個（4セクション＋まとめで5個以上の想定）")

    # リンク
    used_actions = set()
    for href, attrs, label in p.links:
        label = label.strip()
        if href.startswith("#"):
            continue
        if "city_cr23112" in href:
            rep.error("名古屋市南区のリンクがある（南区はリンクを作らない）")
        if label in ("こちら", "ここ", "こちらをクリック"):
            rep.error(f"アンカーテキストが「{label}」（具体的な名詞句にする）: {href}")
        if href in FIXED_URLS:
            st = attrs.get("style", "")
            if href == "tel:0568703096" and not st.startswith(BTN_COMMON):
                continue  # 本文中の電話番号テキストリンクは可
            if not st.startswith(BTN_COMMON):
                rep.warn(f"CTAボタンの style が見本と違う: {label}")
            elif FIXED_URLS[href] not in st:
                rep.error(f"CTAボタンの導線カラーが違う: {label}")
            if href.startswith("https://lin.ee") and (attrs.get("target") != "_blank" or attrs.get("rel") != "nofollow"):
                rep.warn("LINEボタンに target=\"_blank\" rel=\"nofollow\" がない")
            used_actions.add(href)
        elif href in AREA_URLS:
            ku = AREA_URLS[href]
            if label != f"名古屋市{ku}の仲介手数料無料の賃貸を探す":
                rep.warn(f"エリアリンクのアンカーテキストが規定形でない: 「{label}」→「名古屋市{ku}の仲介手数料無料の賃貸を探す」")
        elif href == STAFF_URL:
            pass
        elif href.startswith(SITE):
            rep.warn(f"一覧にないサイト内URL: {href}（{label}）")
        else:
            rep.error(f"外部URL・他社URLの可能性: {href}（{label}）")
    for href in FIXED_URLS:
        if href not in used_actions:
            rep.error(f"CTAボタンがない: {href}")
    if STAFF_URL not in [h for h, _, _ in p.links]:
        rep.error("監修者プロフィールへのリンクがない")
    if not any(h in AREA_URLS for h, _, _ in p.links):
        rep.error("末尾ウィジェットのエリアリンクがない")

    # 固定文言
    for must in ["背古 涼介", "代表取締役", "不動産キャリア7年", "愛知県知事（1）第26010号",
                 "全日本不動産協会", "この記事でわかること", "詳細はこちらの見出しへ！▼", "詳しく解説していきます！"]:
        if must not in plain:
            rep.error(f"必須の文言「{must}」がない")
    for must in ["相見積もり", "分割", "送迎", "24時間", "オンライン", "SUUMO"]:
        if must not in plain:
            rep.warn(f"会社紹介の項目「{must}」が見つからない")
    for other in re.findall(r"0\d{1,4}-\d{1,4}-\d{3,4}", plain):
        if other != "0568-70-3096":
            rep.error(f"他社らしき電話番号: {other}")

    return p


def check_schema(path, rep, body):
    raw = path.read_text(encoding="utf-8").strip()
    m = re.fullmatch(r'<script type="application/ld\+json">(.*)</script>', raw, re.S)
    if not m:
        rep.error("構造化データが <script type=\"application/ld+json\">…</script> だけになっていない")
        return
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        rep.error(f"JSON の構文エラー: {e}")
        return

    nodes = []

    def walk(o):
        if isinstance(o, dict):
            nodes.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    for key in ("datePublished", "dateModified", "aggregateRating"):
        if any(key in n for n in nodes):
            rep.error(f"構造化データに {key} が入っている")

    def of_type(t):
        return [n for n in nodes if n.get("@type") == t or (isinstance(n.get("@type"), list) and t in n["@type"])]

    for t in ("FAQPage", "Article", "BreadcrumbList", "RealEstateAgent"):
        if not of_type(t):
            rep.error(f"構造化データに {t} がない")

    for faq in of_type("FAQPage")[:1]:
        qs = faq.get("mainEntity", [])
        if len(qs) != 4:
            rep.error(f"FAQPage の mainEntity が {len(qs)} 件（4件必要）")
        for i, q in enumerate(qs, 1):
            ans = (q.get("acceptedAnswer") or {}).get("text", "")
            if not (40 <= len(ans) <= 80):
                rep.warn(f"FAQ{i} の回答が {len(ans)} 文字（40〜80文字）")
            if body is not None and body.faq_q:
                name = q.get("name", "")
                if not any(name.strip("Q：: ") in fq or fq.strip("Q：: ") in name for fq in body.faq_q):
                    rep.warn(f"FAQ{i} の質問「{name}」が本文のFAQ目次と一致しない")

    for art in of_type("Article")[:1]:
        author = art.get("author") or {}
        if isinstance(author, list):
            author = author[0] if author else {}
        if author.get("name", "").replace("　", " ") != "背古 涼介" or author.get("url") != STAFF_URL:
            rep.error("Article.author が 背古 涼介／プロフィールURL になっていない")
        pub = art.get("publisher") or {}
        if "くじらのゼロ賃貸" not in pub.get("name", ""):
            rep.error("Article.publisher の name が違う")
        if "logo/logo.png" not in json.dumps(pub.get("logo", ""), ensure_ascii=False):
            rep.error("Article.publisher.logo が違う")
        if not art.get("headline"):
            rep.error("Article.headline がない")

    for bc in of_type("BreadcrumbList")[:1]:
        items = bc.get("itemListElement", [])
        if len(items) != 4:
            rep.warn(f"BreadcrumbList が {len(items)} 階層（トップ＞ブログ＞カテゴリ＞記事 の4階層）")
        urls = [json.dumps(i, ensure_ascii=False) for i in items]
        if len(urls) >= 2 and (SITE not in urls[0] or SITE + "blog/" not in urls[1]):
            rep.error("BreadcrumbList の1・2階層目がトップ・ブログのURLになっていない")

    for ra in of_type("RealEstateAgent")[:1]:
        s = json.dumps(ra, ensure_ascii=False)
        for must in ["くじらのゼロ賃貸", "485-0068", "小牧市", "0568-70-3096", "名古屋市", SITE]:
            if must not in s:
                rep.error(f"RealEstateAgent に「{must}」がない")
        if "Wednesday" in json.dumps(ra.get("openingHoursSpecification", ""), ensure_ascii=False):
            rep.error("RealEstateAgent の営業曜日に水曜（定休日）が入っている")
        if "10:00" not in s or "19:00" not in s:
            rep.error("RealEstateAgent の営業時間 10:00〜19:00 がない")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    target = Path(sys.argv[1])
    if target.is_dir():
        bodies = sorted(target.glob("*_本文.html"))
        schemas = sorted(target.glob("*_構造化データ.html"))
        body_path = bodies[0] if bodies else None
        schema_path = schemas[0] if schemas else None
    else:
        body_path = target
        schema_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    rep = Report()
    body = None
    if body_path and body_path.exists():
        body = check_body(body_path, rep)
    else:
        rep.error("本文HTML（*_本文.html）が見つからない")
    if schema_path and schema_path.exists():
        check_schema(schema_path, rep, body)
    else:
        rep.error("構造化データ（*_構造化データ.html）が見つからない")
    if target.is_dir() and not (target / "レポート.md").exists():
        rep.warn("レポート.md がない")

    for e in rep.errors:
        print("ERROR  ", e)
    for w in rep.warnings:
        print("WARNING", w)
    print(f"\n結果: ERROR {len(rep.errors)} 件 / WARNING {len(rep.warnings)} 件")
    sys.exit(1 if rep.errors else 0)


if __name__ == "__main__":
    main()
