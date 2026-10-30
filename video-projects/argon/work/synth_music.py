import numpy as np, subprocess, os

SR = 44100
TOTAL = 181.608
BPM = 112.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
t = np.arange(int(TOTAL * SR)) / SR
L = np.zeros_like(t); R = np.zeros_like(t)

# Am - F - C - G, one chord per bar
CHORDS = [
    (110.00, [261.63, 329.63, 440.00, 523.25]),   # Am
    (87.31,  [174.61, 220.00, 261.63, 349.23]),   # F
    (130.81, [196.00, 261.63, 329.63, 392.00]),   # C
    (98.00,  [196.00, 246.94, 293.66, 392.00]),   # G
]
n_bars = int(np.ceil(TOTAL / BAR))
rng = np.random.default_rng(42)

def add(sig_l, sig_r, wave, start, gain_l, gain_r):
    i0 = int(start * SR); i1 = min(len(sig_l), i0 + len(wave))
    if i0 >= len(sig_l): return
    w = wave[:i1 - i0]
    sig_l[i0:i1] += w * gain_l; sig_r[i0:i1] += w * gain_r

for bar in range(n_bars):
    root, tones = CHORDS[bar % 4]
    bs = bar * BAR
    # pad: chord tones, slow attack/release across the bar + overlap
    padlen = int((BAR + 0.4) * SR)
    pt = np.arange(padlen) / SR
    env = np.minimum(1, pt / 0.5) * np.minimum(1, np.maximum(0, (BAR + 0.4 - pt) / 0.6))
    pad = np.zeros(padlen)
    for f in tones:
        pad += np.sin(2 * np.pi * f * pt) + 0.4 * np.sin(2 * np.pi * f * 2 * pt)
    pad *= env / len(tones)
    add(L, R, pad, bs, 0.055, 0.055)
    # bass: roots on beats 1, 2.5, 3, 4
    for b_off, blen in [(0, 0.9), (1.5 * BEAT, 0.4), (2 * BEAT, 0.7), (3.5 * BEAT, 0.4)]:
        bl = int(blen * SR); bt = np.arange(bl) / SR
        benv = np.exp(-bt * 5) * np.minimum(1, bt / 0.01)
        bw = np.sin(2 * np.pi * root * bt) * benv
        add(L, R, bw, bs + b_off, 0.11, 0.11)
    # arp: 8th notes cycling chord tones one octave up
    for e in range(8):
        f = tones[e % len(tones)] * 2
        al = int(0.22 * SR); at = np.arange(al) / SR
        aenv = np.exp(-at * 14) * np.minimum(1, at / 0.005)
        aw = (np.sin(2 * np.pi * f * at) + 0.3 * np.sin(2 * np.pi * f * 3 * at)) * aenv
        pan = 0.03 if e % 2 == 0 else 0.05
        add(L, R, aw, bs + e * BEAT / 2, pan, 0.08 - pan)
    # kick on 1 and 3
    for b_off in [0, 2 * BEAT]:
        kl = int(0.14 * SR); kt = np.arange(kl) / SR
        kfreq = 45 + 75 * np.exp(-kt * 40)
        kph = np.cumsum(2 * np.pi * kfreq / SR)
        kw = np.sin(kph) * np.exp(-kt * 22)
        add(L, R, kw, bs + b_off, 0.20, 0.20)
    # hats on offbeat 8ths
    for e in [1, 3, 5, 7]:
        hl = int(0.04 * SR)
        hw = rng.standard_normal(hl) * np.exp(-np.arange(hl) / SR * 160)
        # crude highpass: diff
        hw = np.diff(hw, prepend=0)
        add(L, R, hw, bs + e * BEAT / 2, 0.012, 0.012)

# global fades
fade_in = np.minimum(1, t / 0.4)
fade_out = np.minimum(1, np.maximum(0, (TOTAL - t) / 2.5))
g = fade_in * fade_out * 0.8
L *= g; R *= g
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
if peak > 0.9: L *= 0.9 / peak; R *= 0.9 / peak
stereo = np.stack([L, R], axis=1)
pcm = (np.clip(stereo, -1, 1) * 32767).astype(np.int16)
pcm.tofile('work/music.raw')
subprocess.run(['ffmpeg', '-v', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '2',
                '-i', 'work/music.raw', '-codec:a', 'libmp3lame', '-b:a', '192k',
                '-y', 'assets/audio/music.mp3'], check=True)
os.remove('work/music.raw')
print('music.mp3 written, peak', peak)
