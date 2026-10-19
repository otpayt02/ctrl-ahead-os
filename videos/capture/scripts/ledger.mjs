// Writes manifest_slots-shaped entries into the video's evidence ledger,
// consumed by the renderer's existing evidence-slot merge.
import fs from 'node:fs';
import path from 'node:path';

const cfg = JSON.parse(fs.readFileSync('capture.config.json', 'utf8'));

export function addEntry(entry) {
  const file = cfg.outputs.ledger;
  let items = [];
  if (fs.existsSync(file)) {
    try { items = JSON.parse(fs.readFileSync(file, 'utf8')); } catch { items = []; }
  }
  const stamp = new Date().toISOString().replace(/[-:TZ.]/g, '').slice(0, 14);
  const record = {
    id: `CAP-${stamp}-${String(items.length).padStart(3, '0')}`,
    ...entry,
    provenance: {captured_by: 'ctrl-ahead-capture', at: new Date().toISOString(), ...(entry.provenance ?? {})},
  };
  items.push(record);
  fs.mkdirSync(path.dirname(file), {recursive: true});
  fs.writeFileSync(file, JSON.stringify(items, null, 2));
  console.log(`ledger + ${record.id} -> ${file}`);
  return record;
}
