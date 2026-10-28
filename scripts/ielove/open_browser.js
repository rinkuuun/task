#!/usr/bin/env node
// 自動化専用のブラウザ（ログイン状態を保存するプロファイル）を開く。
// 初回はここで本人がいえらぶCLOUDにログインし、ウィンドウを閉じる。
// 以降の自動化スクリプトは同じプロファイルを使うので、ID・パスワードを扱わない。
//
// 使い方: node scripts/ielove/open_browser.js [開くURL]
const path = require("path");
const os = require("os");
const { chromium } = require("playwright");

const PROFILE = process.env.KUJIRA_BROWSER_PROFILE || path.join(os.homedir(), "kujira-automation", "browser-profile");

async function launch() {
  const opts = { headless: false, viewport: null };
  try {
    return await chromium.launchPersistentContext(PROFILE, { ...opts, channel: "chrome" });
  } catch {
    return await chromium.launchPersistentContext(PROFILE, opts);
  }
}

module.exports = { PROFILE, launch };

if (require.main === module) {
  (async () => {
    const ctx = await launch();
    const page = ctx.pages()[0] || (await ctx.newPage());
    if (process.argv[2]) await page.goto(process.argv[2]);
    console.log(`プロファイル: ${PROFILE}\nログインが済んだらブラウザのウィンドウを閉じてください。`);
    await new Promise((r) => ctx.on("close", r));
  })();
}
