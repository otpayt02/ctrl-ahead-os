// Generic screenshot: node scripts/snap.mjs --url <url> [--site google] [--text "..."] [--sel "..."] [--out name.png] [--scene S6] [--note "..."]
import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import {addEntry} from './ledger.mjs';

const args = process.argv.slice(2);
const arg = (name, fallback) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : fallback; };
const cfg = JSON.parse(fs.readFileSync('capture.config.json', 'utf8'));
const url = arg('--url');
if (!url) {
  console.error('usage: node scripts/snap.mjs --url <url> [--site google] [--text "..."] [--sel "..."] [--out name.png] [--scene S6] [--note "..."]');
  process.exit(1);
}
const site = arg('--site', 'google');
const outName = arg('--out', `snap-${Date.now()}.png`);
const out = `${cfg.outputs.assets}/${outName}`;
fs.mkdirSync(cfg.outputs.assets, {recursive: true});

const ctx = await chromium.launchPersistentContext(`auth/profile-${site}`, {
  headless: false, viewport: {width: 1600, height: 1000}, deviceScaleFactor: 2,
});
const page = ctx.pages()[0] ?? (await ctx.newPage());
await page.goto(url, {waitUntil: 'domcontentloaded'});
await page.waitForTimeout(3000);
const text = arg('--text'), sel = arg('--sel');
if (text) {
  const el = page.getByText(text, {exact: false}).first();
  await el.waitFor({state: 'visible', timeout: 60000});
  await el.scrollIntoViewIfNeeded();
} else if (sel) {
  await page.locator(sel).first().waitFor({state: 'visible', timeout: 60000});
}
await page.screenshot({path: out, fullPage: !text && !sel});
await ctx.close();
console.log(`Saved ${out}`);

addEntry({
  scene_id: arg('--scene'), start: 0, end: 8, type: 'screen', asset: `assets/${path.basename(out)}`,
  text: arg('--note') ?? url, provenance: {url},
});
