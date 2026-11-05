import {useEffect, useMemo} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {BufferAttribute, CatmullRomCurve3, Color, TubeGeometry, Vector3} from 'three';
import {phase, sampleSignal, seeded, type BrandProps} from './motion';

const SAMPLES = 144;
const RADIAL_SEGMENTS = 6;
const toWorld = (x: number, y: number, z: number) => new Vector3(x - 540, 960 - y, z);

const Strand = ({index, seconds, settings}: {index: number; seconds: number; settings: BrandProps}) => {
  const geometry = useMemo(() => {
    const frontier = 145 + 535 * phase(seconds, 0.15, 2.45);
    const samples = Array.from({length: SAMPLES + 1}, (_, n) =>
      sampleSignal(72 + (frontier - 72) * n / SAMPLES, index, seconds, settings));
    const curve = new CatmullRomCurve3(samples.map((p) => toWorld(p.x, p.y, p.z)));
    const tube = new TubeGeometry(curve, SAMPLES, index % 3 === 0 ? 2.8 : 2.1, RADIAL_SEGMENTS, false);
    const colors = new Float32Array(tube.attributes.position.count * 4);
    const base = new Color(index % 3 === 0 ? settings.palette.gold : index % 3 === 1 ? settings.palette.purple : settings.palette.emerald);
    const output = new Color(settings.palette.emerald);
    for (let vertex = 0; vertex < tube.attributes.position.count; vertex++) {
      const fraction = Math.floor(vertex / (RADIAL_SEGMENTS + 1)) / SAMPLES;
      const p = sampleSignal(72 + (frontier - 72) * fraction, index, seconds, settings);
      const color = base.clone().lerp(output, phase(p.x, 390, 650) * phase(seconds, 1.3, 3.3));
      colors.set([color.r, color.g, color.b, p.alpha * phase(seconds, 0, 0.45)], vertex * 4);
    }
    tube.setAttribute('color', new BufferAttribute(colors, 4));
    return tube;
  }, [index, seconds, settings]);
  useEffect(() => () => geometry.dispose(), [geometry]);
  return <mesh geometry={geometry}>
    <meshStandardMaterial vertexColors transparent depthWrite={false} roughness={0.42} metalness={0.18} emissive="#171923" />
  </mesh>;
};

export const SignalField = ({seconds, settings}: {seconds: number; settings: BrandProps}) => (
  <ThreeCanvas width={1080} height={1920} orthographic
    camera={{position: [0, 0, 2000], zoom: 1, near: 0.1, far: 4000}}
    gl={{alpha: true, antialias: true}} dpr={1}
    style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
    <ambientLight intensity={1.4} />
    <directionalLight position={[-300, 500, 700]} intensity={2.1} />
    <directionalLight position={[400, -100, 300]} intensity={0.6} color={settings.palette.purple} />
    {Array.from({length: settings.waveCount}, (_, index) =>
      <Strand key={index} index={index} seconds={seconds} settings={settings} />)}
    {Array.from({length: settings.waveCount * 2}, (_, index) => {
      const wave = index % settings.waveCount;
      const progress = (seeded(settings.seed, 100 + index) + seconds * 0.20) % 1;
      const x = 85 + progress * 575;
      const sample = sampleSignal(x, wave, seconds, settings);
      const frontier = 145 + 535 * phase(seconds, 0.15, 2.45);
      const opacity = sample.alpha * phase(seconds, 0.3, 0.9) * (1 - phase(x, frontier - 25, frontier));
      return <mesh key={index} position={toWorld(x, sample.y, sample.z + 3)}>
        <sphereGeometry args={[index % 4 === 0 ? 4.4 : 3, 10, 8]} />
        <meshBasicMaterial color={index % 3 === 0 ? settings.palette.gold : settings.palette.emerald}
          transparent opacity={opacity} depthWrite={false} />
      </mesh>;
    })}
  </ThreeCanvas>
);
