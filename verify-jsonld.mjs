import fs from 'fs';
import path from 'path';

const dir = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
let bad = 0;
for (const f of files) {
  const html = fs.readFileSync(path.join(dir, f), 'utf8');
  const blocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
  let ok = true; const types = [];
  for (const b of blocks) {
    try { const j = JSON.parse(b[1]); types.push(j['@type']); }
    catch (e) { ok = false; types.push('PARSE-ERR'); }
  }
  if (!ok) bad++;
  console.log(f.padEnd(28), 'blocks=' + blocks.length, 'types=[' + types.join(', ') + ']');
}
console.log(bad ? 'BAD FILES: ' + bad : 'ALL JSON-LD PARSED OK');

// sanity: the machine-readable copy
const sd = JSON.parse(fs.readFileSync(path.join(dir, 'structured-data.json'), 'utf8'));
console.log('structured-data.json ->', sd.map(o => o['@type']).join(', '));
