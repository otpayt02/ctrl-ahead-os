export type Palette = {
  background: string;
  gold: string;
  purple: string;
  emerald: string;
  ivory: string;
};

export type BrandProps = {
  seed: number;
  waveCount: number;
  amplitudes: number[];
  convergenceIntervals: [number, number][];
  durationSeconds: number;
  fps: number;
  palette: Palette;
};

export const clamp = (n: number, min = 0, max = 1) => Math.min(max, Math.max(min, n));
export const smooth = (n: number) => {
  const u = clamp(n);
  return u * u * u * (u * (u * 6 - 15) + 10);
};
export const phase = (seconds: number, start: number, end: number) =>
  smooth((seconds - start) / (end - start));

// Integer hash: seeking to a frame never depends on previously rendered frames.
export const seeded = (seed: number, index: number) => {
  let n = (seed ^ Math.imul(index + 1, 0x9e3779b9)) >>> 0;
  n = Math.imul(n ^ (n >>> 16), 0x21f0aaad);
  n = Math.imul(n ^ (n >>> 15), 0x735a2d97);
  return ((n ^ (n >>> 15)) >>> 0) / 4294967296;
};

export const validateBrand = (props: BrandProps) => {
  const fail = (message: string): never => {throw new Error(`Brand manifest: ${message}`);};
  if (!Number.isSafeInteger(props.seed)) fail('seed must be a safe integer');
  if (!Number.isInteger(props.waveCount) || props.waveCount < 3 || props.waveCount > 18)
    fail('waveCount must be an integer from 3 to 18');
  if (!Number.isFinite(props.durationSeconds) || props.durationSeconds < 3 || props.durationSeconds > 30)
    fail('durationSeconds must be between 3 and 30');
  if (!Number.isInteger(props.fps) || props.fps < 12 || props.fps > 60)
    fail('fps must be an integer from 12 to 60');
  if (!Array.isArray(props.amplitudes) || props.amplitudes.length === 0 ||
    props.amplitudes.some((a) => !Number.isFinite(a) || a < 8 || a > 80))
    fail('amplitudes must contain values from 8 to 80 pixels');
  if (!Array.isArray(props.convergenceIntervals) || props.convergenceIntervals.length < 3)
    fail('provide at least three staggered convergence intervals');
  for (const interval of props.convergenceIntervals) {
    if (!Array.isArray(interval) || interval.length !== 2) fail('each interval needs two x coordinates');
    const [start, end] = interval;
    if (!Number.isFinite(start) || !Number.isFinite(end) || start < 290 || end > 675 || end - start < 140)
      fail('intervals must span at least 140px inside x=290..675');
  }
  if (new Set(props.convergenceIntervals.map(([a, b]) => `${a}:${b}`)).size < 3)
    fail('at least three different intervals are required');
  for (const key of ['background', 'gold', 'purple', 'emerald', 'ivory'] as const) {
    if (!/^#[\da-f]{6}$/i.test(props.palette?.[key] ?? '')) fail(`palette.${key} must be a six-digit hex color`);
  }
  return props;
};

export const sharedY = (x: number) => x <= 520 ? 780 : 780 - ((x - 520) ** 2) / 320;
export const OUTPUT = {start: [680, 700], end: [930, 450]} as const;

export type SignalSample = {x: number; y: number; z: number; alpha: number; alignment: number};

export const sampleSignal = (x: number, index: number, seconds: number, props: BrandProps): SignalSample => {
  const [start, end] = props.convergenceIntervals[index % props.convergenceIntervals.length];
  const aligned = phase(seconds, 1.15, 3.15);
  const alignment = smooth((x - start) / (end - start)) * aligned;
  const amplitude = props.amplitudes[index % props.amplitudes.length];
  const frequency = 0.022 + seeded(props.seed, index * 4) * 0.016;
  const offset = (index / Math.max(1, props.waveCount - 1) - 0.5) * 100;
  const angle = x * frequency - seconds * (1.5 + seeded(props.seed, index * 4 + 1)) +
    seeded(props.seed, index * 4 + 2) * Math.PI * 2;
  // Two frequencies retain an organic input; both vanish with the same smooth envelope.
  const chaos = offset + amplitude * Math.sin(angle) + 0.16 * amplitude * Math.sin(angle * 1.7 + 0.4);
  const visibility = 1 - phase(seconds, 4.2, 5.2) * 0.62;
  return {
    x,
    y: sharedY(x) + chaos * (1 - alignment),
    z: Math.sin(angle * 0.64) * 18 * (1 - alignment),
    alpha: phase(x, 72, 132) * (1 - phase(x, end - 90, end + 8)) * visibility,
    alignment,
  };
};

export const narrativeSeconds = (frame: number, fps: number, duration: number) =>
  (frame / fps) * (6 / duration);
