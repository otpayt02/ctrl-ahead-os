const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

const out = path.resolve(__dirname, '../001-ai-lost-cause/assets/captures');
fs.mkdirSync(out, {recursive: true});
const pages = [
  ['lost-cause', 'https://encyclopediavirginia.org/entries/lost-cause-the/', 'Lost Cause answers: both models rejected the flattering textbook framing and supplied sources.'],
  ['united-daughters', 'https://encyclopediavirginia.org/entries/united-daughters-of-the-confederacy/', 'Lost Cause answer: Sonnet spread citations across secondary pages.'],
  ['atlanta-textbooks', 'https://www.atlantahistorycenter.com/blog/spreading-memory-georgia-history-textbooks-and-the-lost-cause/', 'Lost Cause answer: Sonnet spread citations across secondary pages.'],
  ['mississippi-declaration', 'https://avalon.law.yale.edu/19th_century/csa_missec.asp', "Lost Cause answer: the second model placed Mississippi's 1861 declaration under the slavery claim."],
  ['omniglot-karen', 'https://www.omniglot.com/writing/karen.htm', 'S’gaw Karen answer: Sonnet gave about 2 million speakers from Omniglot.'],
  ['wikipedia-sgaw', 'https://en.wikipedia.org/wiki/S%27gaw_Karen_language', 'S’gaw Karen answer: Sonnet gave 2.2 million speakers from Wikipedia.'],
  ['oxford-sgaw', 'https://www.oxfordreference.com/display/10.1093/acref/9780195139778.001.0001/acref-9780195139778-e-0541', 'S’gaw Karen answer: Sonnet gave 1,050,000 speakers from Oxford Reference.'],
  ['google-privacy', 'https://research.google/blog/privacy-considerations-in-large-language-models/', 'S’gaw Karen answer: the second model cited a general Google Research memorization page, not a S’gaw measurement.'],
];

async function main() {
  const browser = await chromium.launch({headless: true});
  const results = [];
  for (const [name, url, summarySentence] of pages) {
    const page = await browser.newPage({viewport: {width: 1920, height: 1080}, deviceScaleFactor: 1});
    const openedAt = new Date().toISOString();
    const record = {name, requested_url: url, opened_at_utc: openedAt, tool: 'Playwright Chromium', model_reply_sentence: null, model_test_summary_paraphrase: summarySentence, summary_provenance: 'Owner-provided test summary; raw model reply unavailable locally', status: 'pending', visible_text: null, files: []};
    try {
      const response = await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 45000});
      await page.waitForTimeout(1500);
      record.final_url = page.url();
      record.http_status = response?.status() ?? null;
      const body = await page.locator('body').innerText({timeout: 10000});
      const text = body.replace(/\s+/g, ' ').trim();
      record.visible_text = text.slice(0, 320);
      if (!text || (record.http_status && record.http_status >= 500)) throw new Error('Article body not visible or server error');
      const blocked = /subscribe to read|sign in to read|login to view|institutional access|access denied|verify you are human/i.test(text.slice(0, 1400)) || record.http_status === 403;
      record.status = blocked ? 'blocked' : 'loaded';
      const full = `${name}.full.jpg`, viewport = `${name}.png`;
      await page.screenshot({path: path.join(out, full), fullPage: true, type: 'jpeg', quality: 75, animations: 'disabled'});
      if (!blocked && name === 'atlanta-textbooks') {
        const paragraph = page.locator('article p').first();
        if (await paragraph.count()) await paragraph.scrollIntoViewIfNeeded();
      }
      await page.screenshot({path: path.join(out, viewport), type: 'png', animations: 'disabled'});
      record.files = [full, viewport];
    } catch (error) {
      record.error = String(error.message || error);
    }
    results.push(record);
    console.log(`${name}: ${record.status} ${record.http_status ?? ''} ${record.files.join(', ')}`);
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(out, 'provenance.json'), JSON.stringify(results, null, 2) + '\n');
}
main().catch(error => {console.error(error); process.exitCode = 1;});
