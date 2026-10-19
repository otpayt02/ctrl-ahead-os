// Opens the KOA v4 tracker in Drive with your session, spotlights the provenance
// row in amber, and screenshots it into the video assets.
import {chromium} from 'playwright';
import fs from 'node:fs';
import {addEntry} from './ledger.mjs';

const cfg = JSON.parse(fs.readFileSync('capture.config.json', 'utf8'));
const t = cfg.tracker;
const out = `${cfg.outputs.assets}/${t.out}`;
fs.mkdirSync(cfg.outputs.assets, {recursive: true});

const ctx = await chromium.launchPersistentContext('auth/profile-google', {
  headless: false, viewport: {width: 1600, height: 1000}, deviceScaleFactor: 2,
});
const page = ctx.pages()[0] ?? (await ctx.newPage());
await page.goto(`https://drive.google.com/file/d/${t.drive_file_id}/view`, {waitUntil: 'domcontentloaded'});
const row = page.getByText(t.row_hint, {exact: false}).first();
await row.waitFor({state: 'visible', timeout: 90000});
await row.scrollIntoViewIfNeeded();
await row.evaluate((el) => {
  el.style.outline = '5px solid #e8a33d';
  el.style.outlineOffset = '8px';
  el.style.background = '#e8a33d22';
});
await page.waitForTimeout(400);
const box = await row.boundingBox();
const x = Math.max(0, box.x - 260), y = Math.max(0, box.y - 170);
const clip = {x, y, width: Math.min(1600 - x, box.width + 520), height: Math.min(1000 - y, box.height + 340)};
await page.screenshot({path: out, clip});
await ctx.close();
console.log(`Saved ${out}`);

addEntry({
  scene_id: 'S6', start: 0, end: 10, type: 'screen', asset: `assets/${t.out}`,
  text: t.row_hint,
  annotation: {reason: 'S6 evidence: KOA v4 project tracker row for provenance.'},
  provenance: {drive_file_id: t.drive_file_id, drive_view: `https://drive.google.com/file/d/${t.drive_file_id}/view`},
});
