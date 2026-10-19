// One-time login per site. Session persists in auth/profile-<site> (gitignored).
import {chromium} from 'playwright';
import fs from 'node:fs';

const site = process.argv[2];
if (!site) { console.error('usage: node scripts/auth-login.mjs <chatgpt|gemini|claude|google>'); process.exit(1); }
const cfg = JSON.parse(fs.readFileSync('capture.config.json', 'utf8'));
const url = cfg.sites[site]?.url;
if (!url) { console.error(`Unknown site "${site}" — add it to capture.config.json sites.`); process.exit(1); }
fs.mkdirSync('auth', {recursive: true});
const ctx = await chromium.launchPersistentContext(`auth/profile-${site}`, {
  headless: false,
  viewport: {width: 1280, height: 860},
});
const page = ctx.pages()[0] ?? (await ctx.newPage());
await page.goto(url, {waitUntil: 'domcontentloaded'});
console.log(`Log in as ${site} in the opened window, then close the window to finish. The session persists.`);
ctx.on('close', () => process.exit(0));
