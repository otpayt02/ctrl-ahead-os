// Records the same question in two model UIs with your logged-in sessions,
// then composites both side-by-side into a 1920x1080 MP4 and writes the ledger entry.
import {chromium} from 'playwright';
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {addEntry} from './ledger.mjs';

const cfg = JSON.parse(fs.readFileSync('capture.config.json', 'utf8'));
const demo = cfg.model_demo;
fs.mkdirSync(cfg.outputs.tmp, {recursive: true});

const waitSettle = async (page) => {
  const {stable_ms, timeout_ms} = demo.settle;
  let last = -1, lastChange = Date.now();
  const deadline = Date.now() + timeout_ms;
  while (Date.now() < deadline) {
    await page.waitForTimeout(2000);
    const len = await page.evaluate(() => document.body.innerText.length).catch(() => last);
    if (len !== last) { last = len; lastChange = Date.now(); }
    if (Date.now() - lastChange > stable_ms) return;
  }
};

const clips = [];
for (const site of demo.sites) {
  console.log(`Recording ${site.name}...`);
  const ctx = await chromium.launchPersistentContext(`auth/profile-${site.name}`, {
    headless: false,
    viewport: {width: 960, height: 1080},
    recordVideo: {dir: cfg.outputs.tmp, size: {width: 960, height: 1080}},
  });
  const page = ctx.pages()[0] ?? (await ctx.newPage());
  await page.goto(site.url, {waitUntil: 'domcontentloaded'});
  await page.waitForTimeout(site.warmup_ms ?? 4000);
  const input = page.locator(site.input_selector).first();
  await input.waitFor({state: 'visible', timeout: 90000});
  await input.click();
  await page.keyboard.type(demo.question, {delay: 20});
  await page.keyboard.press('Enter');
  const video = page.video();
  await waitSettle(page);
  await page.waitForTimeout(2500);
  const rawPath = await video.path();
  await ctx.close();
  clips.push({name: site.name, path: rawPath});
  console.log(`  captured ${rawPath}`);
}

const bundled = '../render/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe';
const ffmpeg = process.env.FFMPEG_PATH || (fs.existsSync(bundled) ? bundled : 'ffmpeg');
const out = `${cfg.outputs.assets}/${demo.out}`;
fs.mkdirSync(cfg.outputs.assets, {recursive: true});
execFileSync(ffmpeg, [
  '-y', '-i', clips[0].path, '-i', clips[1].path,
  '-filter_complex',
  '[0:v]scale=960:-2,setsar=1,pad=960:1080:(ow-iw)/2:(oh-ih)/2:black[a];[1:v]scale=960:-2,setsar=1,pad=960:1080:(ow-iw)/2:(oh-ih)/2:black[b];[a][b]hstack=inputs=2',
  '-r', '30', '-c:v', 'libx264', '-crf', '22', '-pix_fmt', 'yuv420p', out,
], {stdio: 'inherit'});
console.log(`Composited ${out}`);

addEntry({
  scene_id: 'S4', start: 0, end: 110, type: 'screen-recording', asset: `assets/${demo.out}`,
  text: `Live two-model comparison recorded via Playwright (${clips.map((c) => c.name).join(' vs ')}).`,
  annotation: {reason: 'S4 evidence: same question asked to two models to compare citation behavior.'},
  provenance: {tool: 'playwright', question: demo.question},
});
