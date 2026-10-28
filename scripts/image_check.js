#!/usr/bin/env node
// いえらぶCLOUD 表紙画像の条件チェック: JPG/JPEG のみ・10MB 未満（3MB 以上はサイズが変わる可能性あり）
// 使い方: node scripts/image_check.js <画像ファイル>
const fs = require("fs");
const f = process.argv[2];
if (!f || !fs.existsSync(f)) { console.error("ERROR 画像ファイルがない"); process.exit(1); }
const buf = fs.readFileSync(f);
const mb = buf.length / 1024 / 1024;
let ok = true;
if (!/\.jpe?g$/i.test(f) || buf[0] !== 0xff || buf[1] !== 0xd8) { console.log("ERROR JPG/JPEG 形式ではない"); ok = false; }
if (mb >= 10) { console.log(`ERROR ${mb.toFixed(2)}MB（10MB 未満にする）`); ok = false; }
else if (mb >= 3) console.log(`WARNING ${mb.toFixed(2)}MB（3MB 以上はいえらぶ側でサイズが変わる可能性あり）`);
console.log(`${ok ? "OK" : "NG"} ${f} ${mb.toFixed(2)}MB`);
process.exit(ok ? 0 : 1);
