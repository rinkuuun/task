#!/usr/bin/env node
// Claude Code のステータスライン。利用状況（5時間・週間）を表示し、
// usage_check.js が読めるように .claude/usage.json に書き出す。
const fs = require("fs");
const path = require("path");

let raw = "";
process.stdin.on("data", (c) => (raw += c));
process.stdin.on("end", () => {
  let data = {};
  try {
    data = JSON.parse(raw);
  } catch {}
  const dir = (data.workspace && data.workspace.project_dir) || data.cwd || process.cwd();
  const rl = data.rate_limits;
  if (rl) {
    try {
      fs.writeFileSync(
        path.join(dir, ".claude", "usage.json"),
        JSON.stringify({ updated_at: new Date().toISOString(), rate_limits: rl }, null, 2)
      );
    } catch {}
  }
  const pct = (w) => (w && typeof w.used_percentage === "number" ? `${Math.round(w.used_percentage)}%` : "-");
  process.stdout.write(rl ? `週 ${pct(rl.seven_day)} ・ 5時間 ${pct(rl.five_hour)}` : "利用状況: 取得待ち");
});
