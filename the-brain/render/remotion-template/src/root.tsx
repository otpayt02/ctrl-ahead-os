import React from 'react';
import {AbsoluteFill, Composition, interpolate, Sequence, useCurrentFrame, useVideoConfig} from 'remotion';
import manifest from '../sample-manifest.json';

type Scene = {index:number; start_frame:number; duration_frames:number; visual_prompt:string; narration:string; music_cue:string; on_screen_text:string; human_face:boolean; asset_path:string|null};
type Manifest = {title:string; fps:number; width:number; height:number; duration_frames:number; scenes:Scene[]};
const sample = manifest as Manifest;

const SceneView: React.FC<{scene:Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const opacity = interpolate(frame, [0, Math.min(fps / 2, scene.duration_frames / 2)], [0, 1], {extrapolateRight:'clamp'});
  const shift = interpolate(frame, [0, scene.duration_frames], [28, -18], {extrapolateRight:'clamp'});
  return <AbsoluteFill style={{background:'radial-gradient(circle at 25% 30%, #143c50 0%, #07141f 58%, #03080d 100%)', color:'#f2eee5', fontFamily:'Arial, sans-serif', overflow:'hidden'}}>
    <div style={{position:'absolute', inset:60, border:'1px solid rgba(213,173,111,.35)', borderRadius:24}} />
    <div style={{position:'absolute', top:90, left:105, color:'#d5ad6f', letterSpacing:8, fontSize:19}}>CTRL AHEAD / FIELD NOTES</div>
    <div style={{position:'absolute', left:105, right:105, top:'35%', transform:`translateY(${shift}px)`, opacity, fontSize:70, lineHeight:1.12, fontWeight:700}}>{scene.on_screen_text || scene.narration}</div>
    <div style={{position:'absolute', bottom:105, left:105, right:105, color:'#a7c7d3', fontSize:22}}>SCENE {String(scene.index + 1).padStart(2,'0')} · {scene.human_face ? 'HUMAN FACE REQUIRED' : 'VISUAL ASSET PENDING'}</div>
  </AbsoluteFill>;
};

const Video: React.FC<{data:Manifest}> = ({data}) => <AbsoluteFill>{data.scenes.map(scene => <Sequence key={scene.index} from={scene.start_frame} durationInFrames={scene.duration_frames}><SceneView scene={scene}/></Sequence>)}</AbsoluteFill>;

export const Root: React.FC = () => <Composition id="BrainVideo" component={Video} durationInFrames={sample.duration_frames} fps={sample.fps} width={sample.width} height={sample.height} defaultProps={{data:sample}} />;
