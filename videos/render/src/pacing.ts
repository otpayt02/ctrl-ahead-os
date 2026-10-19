// Pacing engine - implements the rules in videos/FACELESS-VISUAL-SYSTEM.md.
// Deterministic: same manifest + pacing config => identical visual plan on every render.
// The average dwell (0-20s) is the draggable value from videos/pacing-studio.html.

export type PacingConfig = {
  average_dwell_sec: number;
  max_dwell_sec: number;
  jitter: [number, number];
  visual_change_floor_sec: number;
  seed: number;
  presenter_mode?: string;
};

export const DEFAULT_PACING: PacingConfig = {
  average_dwell_sec: 7,
  max_dwell_sec: 15,
  jitter: [0.2, 0.35],
  visual_change_floor_sec: 4,
  seed: 7,
  presenter_mode: 'faceless',
};

export type OverlayBeat = {at: number; kind: string; text: string};
export type VisualBeat = {asset: string; duration_sec: number; motion: string; overlays: OverlayBeat[]};

export function mulberry32(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t);
    t = Math.imul(t ^ (t >>> 7), t | 0x61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const MOTIONS = [
  'push-in 1.02x->1.12x',
  'pull-back 1.16x->1.02x',
  'lateral drift L->R',
  'push-in 1.05x->1.2x',
  'lateral drift R->L',
  'hold + overlay build',
];

const round1 = (n: number) => Math.round(n * 10) / 10;
const clamp = (n: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, n));

function normalizeDurations(durs: number[], total: number, cap: number, lo = 2.5): number[] {
  for (let pass = 0; pass < 8; pass++) {
    const diff = total - durs.reduce((a, b) => a + b, 0);
    if (Math.abs(diff) < 0.05) break;
    const roomy: number[] = [];
    durs.forEach((d, i) => {
      if (diff > 0 ? d < cap - 0.1 : d > lo + 0.1) roomy.push(i);
    });
    if (!roomy.length) break;
    const per = diff / roomy.length;
    roomy.forEach((i) => {
      durs[i] = round1(clamp(durs[i] + per, lo, cap));
    });
  }
  const residual = round1(total - durs.reduce((a, b) => a + b, 0));
  if (Math.abs(residual) >= 0.1) {
    for (let i = 0; i < durs.length; i++) {
      const nd = round1(durs[i] + residual);
      if (nd >= lo && nd <= cap) {
        durs[i] = nd;
        break;
      }
    }
  }
  return durs;
}

export type PaceableScene = {
  start: number;
  end: number;
  assets?: string[];
  producer_note?: string;
  chapter?: string;
  overlay_pool?: string[];
};

export function planSceneVisuals(scene: PaceableScene, cfg: PacingConfig, rand: () => number): VisualBeat[] {
  const D = scene.end - scene.start;
  const target = Math.min(cfg.average_dwell_sec, cfg.max_dwell_sec);
  const n = Math.max(1, Math.round(D / Math.max(target, 2.5)));
  const base = D / n;
  const assets = scene.assets?.length ? scene.assets : ['assets/placeholder.png'];
  const keyScene = Boolean(scene.producer_note) || (scene.chapter ?? '').includes('VERDICT');
  const raw: number[] = [];
  for (let i = 0; i < n; i++) {
    const mag = cfg.jitter[0] + rand() * (cfg.jitter[1] - cfg.jitter[0]);
    const sign = rand() > 0.5 ? 1 : -1;
    const boost = keyScene && i % 3 === 1 ? 1.3 : 1;
    raw.push(clamp(base * (1 + sign * mag * boost), 2.5, cfg.max_dwell_sec));
  }
  const durs = normalizeDurations(raw, D, cfg.max_dwell_sec);
  return durs.map((d, i) => {
    const beats: number[] = [];
    let t = 1.2 + rand() * 1.3;
    while (t < d - 0.8) {
      beats.push(round1(t));
      t += cfg.visual_change_floor_sec + rand() * 1.6;
    }
    const overlays: OverlayBeat[] = [];
    const limit = d > 4.5 ? 2 : 1;
    beats.slice(0, limit).forEach((at, j) => {
      const pool = scene.overlay_pool;
      if (pool?.length) {
        const text = pool[(i + j) % pool.length];
        overlays.push({at, kind: /\d/.test(text) ? 'stat' : 'term', text});
      }
    });
    return {
      asset: assets[i % assets.length],
      duration_sec: d,
      motion: MOTIONS[(i + (keyScene ? 1 : 0)) % MOTIONS.length],
      overlays,
    };
  });
}

export function applyPacing<T extends {pacing?: Partial<PacingConfig>; scenes: PaceableScene[]}>(
  manifest: T,
  override?: Partial<PacingConfig>
): T & {pacing: PacingConfig; scenes: (PaceableScene & {visuals: VisualBeat[]})[]} {
  const cfg: PacingConfig = {...DEFAULT_PACING, ...(manifest.pacing ?? {}), ...(override ?? {})};
  const rand = mulberry32(cfg.seed);
  return {
    ...manifest,
    pacing: cfg,
    scenes: manifest.scenes.map((sc) => ({...sc, visuals: planSceneVisuals(sc, cfg, rand)})),
  };
}
