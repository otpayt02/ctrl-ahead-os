import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validateBrand, sampleSignal, sharedY, OUTPUT} from '../src/brand/motion.ts';

const props = validateBrand(JSON.parse(readFileSync(new URL('../brand-manifest.json', import.meta.url))));
assert.equal(Math.round(props.durationSeconds * props.fps), 180);
const a = sampleSignal(440, 3, 2.1, props);
sampleSignal(600, 8, 5.9, props);
assert.deepEqual(sampleSignal(440, 3, 2.1, props), a, 'seeking must be history independent');
assert.notEqual(sampleSignal(440, 3, 2.1, {...props, seed: 43}).y, a.y);
for (let i = 0; i < props.waveCount; i++) {
  const p = sampleSignal(680, i, 4, props);
  assert.equal(p.y, 700);
  assert.ok(p.z === 0);
  assert.equal(p.alpha, 0);
}
const slope = (sharedY(680) - sharedY(679.999)) / 0.001;
assert.ok(Math.abs(slope + 1) < 0.00001, 'junction tangent must match arrow');
assert.equal(Math.atan2(OUTPUT.start[1] - OUTPUT.end[1], OUTPUT.end[0] - OUTPUT.start[0]) * 180 / Math.PI, 45);
assert.throws(() => validateBrand({...props, waveCount: 99}));
assert.throws(() => validateBrand({...props, convergenceIntervals: [[300, 600], [300, 600], [300, 600]]}));
console.log('PASS: 180 frames; deterministic seeking and seed variation; 9 aligned/faded strand endpoints; continuous junction tangent; 45 degree output; invalid manifests rejected.');
