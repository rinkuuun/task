#!/usr/bin/env node
// 進捗一覧.csv（Excelで開ける UTF-8 BOM 付き CSV）の読み書き。
//
//   node scripts/manifest.js show
//   node scripts/manifest.js add <番号> <タイトル> <編集画面URL>
//   node scripts/manifest.js set <番号> <列名> <値>
//   node scripts/manifest.js next <列名>      … その列が空の最初の行を JSON で出力（なければ終了コード1）
//
// 保存先は環境変数 KUJIRA_WORK_DIR（未設定なら Dropbox の記事作成フォルダ）。
const fs = require("fs");
const path = require("path");
const os = require("os");

const WORK_DIR =
  process.env.KUJIRA_WORK_DIR ||
  path.join(os.homedir(), "Dropbox", "不動産関係", "くじら不動産", "賃貸", "記事作成");
const FILE = path.join(WORK_DIR, "進捗一覧.csv");
const COLS = ["番号", "タイトル", "編集画面URL", "フォルダ", "元記事取得", "リライト", "画像", "公開", "要確認", "メモ"];

function parse(text) {
  const rows = [];
  let row = [], cur = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"' && text[i + 1] === '"') { cur += '"'; i++; }
      else if (c === '"') q = false;
      else cur += c;
    } else if (c === '"') q = true;
    else if (c === ",") { row.push(cur); cur = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(cur); rows.push(row); row = []; cur = "";
    } else cur += c;
  }
  if (cur || row.length) { row.push(cur); rows.push(row); }
  return rows;
}

function load() {
  if (!fs.existsSync(FILE)) return [];
  const rows = parse(fs.readFileSync(FILE, "utf8").replace(/^﻿/, ""));
  const head = rows.shift() || COLS;
  return rows.filter((r) => r.length > 1).map((r) => Object.fromEntries(COLS.map((c) => [c, r[head.indexOf(c)] ?? ""])));
}

function save(items) {
  const esc = (v) => (/[",\r\n]/.test(v) ? `"${String(v).replace(/"/g, '""')}"` : String(v));
  items.sort((a, b) => Number(a["番号"]) - Number(b["番号"]));
  const body = [COLS, ...items.map((it) => COLS.map((c) => it[c] ?? ""))].map((r) => r.map(esc).join(",")).join("\r\n");
  fs.mkdirSync(WORK_DIR, { recursive: true });
  fs.writeFileSync(FILE, "﻿" + body + "\r\n", "utf8");
}

const pad = (n) => String(n).padStart(3, "0");
const safe = (s) => s.replace(/[\\/:*?"<>|]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) + 0xfee0)).trim();

const [cmd, ...args] = process.argv.slice(2);
const items = load();
const find = (n) => items.find((it) => Number(it["番号"]) === Number(n));

if (cmd === "show") {
  for (const it of items) console.log(COLS.map((c) => `${c}:${it[c]}`).join(" | "));
  console.log(`\n${FILE}`);
} else if (cmd === "add") {
  const [n, title, url] = args;
  if (find(n)) { console.error(`${n} は登録済み`); process.exit(1); }
  const folder = `${pad(n)}_${safe(title)}`;
  items.push({ 番号: String(Number(n)), タイトル: title, 編集画面URL: url || "", フォルダ: folder });
  save(items);
  fs.mkdirSync(path.join(WORK_DIR, folder), { recursive: true });
  console.log(path.join(WORK_DIR, folder));
} else if (cmd === "set") {
  const [n, col, ...rest] = args;
  const it = find(n);
  if (!it || !COLS.includes(col)) { console.error("番号または列名が不正"); process.exit(1); }
  it[col] = rest.join(" ");
  save(items);
} else if (cmd === "next") {
  const it = items.find((x) => !x[args[0]]);
  if (!it) process.exit(1);
  console.log(JSON.stringify({ ...it, フォルダパス: path.join(WORK_DIR, it["フォルダ"]) }));
} else {
  console.log(fs.readFileSync(__filename, "utf8").split("\n").slice(1, 9).join("\n"));
}
