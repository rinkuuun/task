#!/usr/bin/env node
// Claude と Codex の週間利用状況を確認する。
// 週間の残りが 30% を切る（使用率 70% 以上）なら作業を止める。
//
// 使い方: node scripts/usage_check.js [上限%=70]
// 終了コード: 0=続行OK / 2=上限に達したので停止 / 3=利用状況が取れない（ユーザーに確認）
const fs = require("fs");
const os = require("os");
const path = require("path");

const LIMIT = Number(process.argv[2] || 70);
const root = path.resolve(__dirname, "..");

function fmtReset(v) {
  if (v == null) return "不明";
  const d = typeof v === "number" ? new Date(v < 1e12 ? v * 1000 : v) : new Date(v);
  return isNaN(d) ? String(v) : d.toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" });
}

function claudeUsage() {
  const f = path.join(root, ".claude", "usage.json");
  if (!fs.existsSync(f)) return null;
  const j = JSON.parse(fs.readFileSync(f, "utf8"));
  const w = j.rate_limits && j.rate_limits.seven_day;
  if (!w || typeof w.used_percentage !== "number") return null;
  const ageMin = Math.round((Date.now() - new Date(j.updated_at)) / 60000);
  return { used: w.used_percentage, reset: fmtReset(w.resets_at), ageMin };
}

function newestJsonl(dir) {
  let best = null;
  const walk = (d) => {
    let ents = [];
    try {
      ents = fs.readdirSync(d, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of ents) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith(".jsonl")) {
        const m = fs.statSync(p).mtimeMs;
        if (!best || m > best.m) best = { p, m };
      }
    }
  };
  walk(dir);
  return best;
}

function codexUsage() {
  const home = process.env.CODEX_HOME || path.join(os.homedir(), ".codex");
  const f = newestJsonl(path.join(home, "sessions"));
  if (!f) return null;
  const lines = fs.readFileSync(f.p, "utf8").trim().split("\n").reverse();
  for (const line of lines) {
    let j;
    try {
      j = JSON.parse(line);
    } catch {
      continue;
    }
    const pl = j.payload || j.msg || j;
    const rl = pl && (pl.rate_limits || pl.rateLimits);
    if (!rl) continue;
    const w = rl.secondary || rl.secondary_window || rl.weekly;
    if (!w) continue;
    const used = w.used_percent ?? w.usedPercent ?? w.used_percentage;
    if (typeof used !== "number") continue;
    const reset = w.resets_at ?? w.resetsAt ?? (w.resets_in_seconds != null ? Date.now() + w.resets_in_seconds * 1000 : null);
    return { used, reset: fmtReset(reset), ageMin: Math.round((Date.now() - f.m) / 60000) };
  }
  return null;
}

let stop = false;
let unknown = false;
for (const [name, fn] of [["Claude", claudeUsage], ["Codex", codexUsage]]) {
  let u = null;
  try {
    u = fn();
  } catch {}
  if (!u) {
    console.log(`${name}: 週間利用状況を取得できません`);
    unknown = true;
    continue;
  }
  const over = u.used >= LIMIT;
  if (over) stop = true;
  console.log(`${name}: 週間 ${u.used}% 使用（残り ${100 - u.used}%）／リセット ${u.reset}／${u.ageMin}分前の値${over ? " → 上限到達" : ""}`);
}
if (stop) {
  console.log(`週間の残りが ${100 - LIMIT}% を切ったため停止してください。`);
  process.exit(2);
}
process.exit(unknown ? 3 : 0);
