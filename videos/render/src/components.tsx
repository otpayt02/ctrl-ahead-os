import React from 'react';
import {AbsoluteFill, Audio, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {MediaInventory, TimelineScene, VideoManifest} from './timeline';
import type {VisualBeat} from './pacing';
import '@fontsource/eb-garamond/400.css';
import '@fontsource/eb-garamond/600.css';
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource/jetbrains-mono/600.css';

const NAVY = '#0a1628', AMBER = '#e8a33d', CYAN = '#c9d6df', PAPER = '#f5efe6';
const DISPLAY = 'EB Garamond, Georgia, serif', DATA = 'JetBrains Mono, monospace';
type SceneProps = {scene: TimelineScene; media: MediaInventory; placeholderMode: boolean; isFirst?: boolean; isLast?: boolean; endCard?: VideoManifest['end_card']};

const Placeholder: React.FC<{label: string}> = ({label}) => <AbsoluteFill style={{background:`linear-gradient(145deg, ${NAVY}, #153449 54%, #06101d)`, display:'grid', placeItems:'center'}}><div style={{width:720, height:380, border:`1px solid ${AMBER}88`, display:'grid', placeItems:'center', boxShadow:'0 0 80px #e8a33d18', fontFamily:DATA, fontSize:23, color:AMBER, letterSpacing:3, textAlign:'center', lineHeight:1.8}}>MEDIA PENDING<br/><span style={{fontSize:17, color:CYAN}}>{label}</span></div></AbsoluteFill>;

const ImagePlane: React.FC<{asset?: string; media: MediaInventory; placeholderMode: boolean}> = ({asset, media, placeholderMode}) => {
  const filename = asset?.startsWith('assets/') ? asset.slice(7) : null;
  const usable = filename && !placeholderMode && media.availableAssets.includes(filename);
  return usable ? <AbsoluteFill><Img src={staticFile(`scene-assets/${filename}`)} style={{width:'100%',height:'100%',objectFit:'cover'}}/></AbsoluteFill> : <Placeholder label={asset ?? 'VERIFIED RECORDING / ARTIFACT'}/>;
};

export const KenBurns: React.FC<SceneProps> = ({scene, media, placeholderMode}) => {
  const frame = useCurrentFrame(), motion = scene.motion?.toLowerCase() ?? '';
  const drift = motion.includes('lateral drift'), reverse = motion.includes('r->l');
  const zoom = motion.match(/(\d+(?:\.\d+)?)x->(\d+(?:\.\d+)?)x/);
  const start = zoom ? Number(zoom[1]) : 1.04, end = zoom ? Number(zoom[2]) : start;
  const scale = interpolate(frame,[0,Math.max(1,scene.durationInFrames-1)],[start,end],{extrapolateRight:'clamp'});
  const x = drift ? interpolate(frame,[0,Math.max(1,scene.durationInFrames-1)],reverse?[50,-50]:[-50,50],{extrapolateRight:'clamp'}) : 0;
  return <AbsoluteFill style={{transform:`translateX(${x}px) scale(${scale})`}}><ImagePlane asset={scene.assets?.find(a=>a.startsWith('assets/'))} media={media} placeholderMode={placeholderMode}/></AbsoluteFill>;
};

export const SplitFrame: React.FC<SceneProps> = ({scene, media, placeholderMode}) => {
  const frame = useCurrentFrame();
  return <AbsoluteFill><KenBurns scene={scene} media={media} placeholderMode={placeholderMode}/><div style={{position:'absolute',left:'50%',top:0,bottom:0,width:5,background:CYAN,boxShadow:`0 0 ${30+10*Math.sin(frame/15)}px ${CYAN}`}}/><div style={{position:'absolute',left:85,bottom:165,padding:'18px 26px',background:'#0a1628bb',fontFamily:DATA,fontSize:24,color:PAPER}}>MEMORY / SOURCE</div><div style={{position:'absolute',right:85,bottom:165,padding:'18px 26px',background:'#0a1628bb',fontFamily:DATA,fontSize:24,color:CYAN}}>MODEL / CORPUS</div></AbsoluteFill>;
};

export const ScreenCapture: React.FC<SceneProps> = ({scene, media, placeholderMode}) => <AbsoluteFill style={{background:NAVY}}><div style={{position:'absolute',inset:'9% 8%',overflow:'hidden',border:`2px solid ${CYAN}77`,borderRadius:22,boxShadow:'0 35px 100px #0009'}}><KenBurns scene={scene} media={media} placeholderMode={placeholderMode}/><div style={{position:'absolute',left:50,right:50,bottom:54,height:5,background:'#c96258',boxShadow:'0 0 25px #c96258'}}/></div><div style={{position:'absolute',left:175,top:140,fontFamily:DATA,color:AMBER,fontSize:22,letterSpacing:4}}>VERIFY THE CLAIM / ORIGINAL RECORDING PENDING</div></AbsoluteFill>;

export const CrossFadeSequence: React.FC<SceneProps> = ({scene, media, placeholderMode}) => {
  const frame = useCurrentFrame(), {fps}=useVideoConfig(), midpoint=Math.round(scene.durationInFrames*.52);
  const blend=interpolate(frame,[midpoint,midpoint+Math.round(1.5*fps)],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const beat = Math.floor(frame/(7*fps)), scale = 1.03 + (frame%(7*fps))/(7*fps)*.035;
  return <AbsoluteFill style={{transform:`scale(${scale}) translateX(${(beat%3-1)*20}px)`}}><ImagePlane asset={scene.assets?.[0]} media={media} placeholderMode={placeholderMode}/><AbsoluteFill style={{opacity:blend}}><ImagePlane asset={scene.assets?.[1]} media={media} placeholderMode={placeholderMode}/></AbsoluteFill></AbsoluteFill>;
};

export const KineticType: React.FC<{text:string; scene:TimelineScene}> = ({text,scene}) => {
  const frame=useCurrentFrame(), {fps}=useVideoConfig(), start=scene.fromFrame===0?8*fps:Math.min(2*fps,Math.round(scene.durationInFrames*.1));
  const opacity=interpolate(frame,[start,start+22],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const spacing=interpolate(frame,[start,start+28],[15,3],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <div style={{position:'absolute',left:112,right:112,bottom:125,padding:'25px 34px',background:'#0a1628c9',borderLeft:`5px solid ${AMBER}`,color:PAPER,fontFamily:DATA,fontWeight:600,fontSize:Math.max(27,46-Math.floor(text.length/15)),lineHeight:1.42,opacity,letterSpacing:spacing,textShadow:'0 3px 16px #000'}}>{text}</div>;
};

export const ChapterCard: React.FC<{scene:TimelineScene}> = ({scene}) => {
  const frame=useCurrentFrame(),opacity=interpolate(frame,[0,12,50,70],[0,1,1,0],{extrapolateRight:'clamp'});
  return <div style={{position:'absolute',left:110,top:92,opacity,color:PAPER,textShadow:'0 3px 20px #000'}}><div style={{fontFamily:DATA,fontSize:19,letterSpacing:5,color:AMBER}}>CHAPTER {scene.id.slice(1).padStart(2,'0')}</div><div style={{fontFamily:DISPLAY,fontSize:70,lineHeight:1.1,marginTop:14}}>{scene.chapter}</div></div>;
};

export const EndCard: React.FC<{scene:TimelineScene; content?:VideoManifest['end_card']}> = ({scene,content}) => {
  const frame=useCurrentFrame(),{fps}=useVideoConfig(),start=Math.max(0,scene.durationInFrames-12*fps);
  const opacity=interpolate(frame,[start,start+20],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <AbsoluteFill style={{opacity,background:NAVY,display:'flex',alignItems:'center',justifyContent:'center',flexDirection:'column',color:PAPER}}><div style={{fontFamily:DISPLAY,fontSize:100}}>{content?.headline??'Keep building.'}</div><div style={{fontFamily:DATA,fontSize:28,letterSpacing:5,color:AMBER,marginTop:35}}>{content?.series??'CTRL AHEAD'}</div><div style={{fontFamily:DATA,fontSize:18,color:CYAN,marginTop:60}}>{content?.teaser??''}</div></AbsoluteFill>;
};

const TakeawayCards: React.FC<{scene:TimelineScene}> = ({scene}) => {
  const frame=useCurrentFrame(),{fps}=useVideoConfig();
  const items=[...((scene.on_screen_text??'').matchAll(/\d+\)\s*([^\d]+?)(?=\s*\d+\)|$)/g))].map(match=>match[1].trim());
  if (!items.length) return null;
  const index=Math.min(items.length-1,Math.floor(Math.max(0,frame-6*fps)/(14*fps)));
  const visible=frame>=6*fps && frame<scene.durationInFrames-12*fps;
  const opacity=visible?interpolate(frame%(14*fps),[0,10],[0,1],{extrapolateRight:'clamp'}):0;
  return visible?<div style={{position:'absolute',left:110,top:'31%',padding:'34px 46px',background:'#0a1628dd',borderLeft:`7px solid ${AMBER}`,fontFamily:DATA,fontSize:52,fontWeight:600,color:PAPER,opacity}}>{index+1}. {items[index]}</div>:null;
};

const FilmTexture: React.FC = () => {
  const phase=useCurrentFrame()%7;
  return <AbsoluteFill style={{pointerEvents:'none',opacity:.44,background:`radial-gradient(ellipse at center, transparent 42%, #0009 100%), repeating-linear-gradient(${91+phase}deg, transparent 0px, #ffffff08 1px, transparent 3px, transparent 7px)`,mixBlendMode:'multiply'}}/>;
};

const PacingChip: React.FC<{visual:VisualBeat; kind:string; text:string; atFrame:number; durationInFrames:number}> = ({visual,kind,text,atFrame,durationInFrames}) => {
  const frame=useCurrentFrame(),{fps}=useVideoConfig();
  const fadeStart=Math.max(atFrame+1,durationInFrames-Math.round(.6*fps));
  const opacity=interpolate(frame,[atFrame,atFrame+Math.round(.3*fps),fadeStart,durationInFrames],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const rise=interpolate(frame,[atFrame,atFrame+Math.round(.45*fps)],[12,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <div data-overlay-kind={kind} data-visual-asset={visual.asset} style={{position:'absolute',left:112,right:112,top:kind==='stat'?310:390,pointerEvents:'none',opacity,transform:`translateY(${rise}px)`,textAlign:'center'}}><span style={{display:'inline-block',maxWidth:'76%',padding:kind==='stat'?'13px 22px':'18px 30px',background:'#0a1628e8',border:`2px solid ${kind==='stat'?CYAN:AMBER}`,color:kind==='stat'?CYAN:PAPER,fontFamily:kind==='stat'?DATA:DISPLAY,fontSize:kind==='stat'?24:42,lineHeight:1.25,boxShadow:'0 14px 38px #0009'}}>{text}</span></div>;
};

const VisualView: React.FC<SceneProps & {visual:VisualBeat; visualFrames:number; visualStart:number}> = ({scene,media,placeholderMode,visual,visualFrames,visualStart}) => {
  const {fps}=useVideoConfig(),kind=scene.component;
  const shot={...scene,assets:[visual.asset],motion:visual.motion,durationInFrames:visualFrames};
  const content=kind.includes('SplitFrame')?<SplitFrame scene={shot} media={media} placeholderMode={placeholderMode}/>:kind.startsWith('ScreenCapture')?<ScreenCapture scene={shot} media={media} placeholderMode={placeholderMode}/>:<KenBurns scene={shot} media={media} placeholderMode={placeholderMode}/>;
  const scale=visualFrames/Math.max(1,visual.duration_sec*fps);
  return <AbsoluteFill>{content}{visual.asset.startsWith('assets/')&&!placeholderMode&&media.availableAssets.includes(visual.asset.slice(7))&&<div style={{position:'absolute',right:70,top:50,padding:'10px 16px',background:'#0a1628dd',border:`1px solid ${CYAN}`,fontFamily:DATA,fontSize:17,letterSpacing:2,color:CYAN}}>AI-GENERATED ILLUSTRATION</div>}{visual.overlays.map((overlay,index)=>{
    const atFrame=Math.round(overlay.at*fps*scale);
    const start=visualStart+atFrame;
    const end=visualStart+visualFrames;
    const collides=scene.manifest_slots?.some(slot=>Math.round((slot.start??0)*fps)<end&&Math.round((slot.end??slot.start??0)*fps)>start);
    return collides?null:<PacingChip key={index} visual={visual} kind={overlay.kind} text={overlay.text} atFrame={atFrame} durationInFrames={visualFrames}/>;
  })}</AbsoluteFill>;
};

const SceneView: React.FC<SceneProps> = ({scene,media,placeholderMode,isFirst,isLast,endCard}) => {
  const frame=useCurrentFrame(),{fps}=useVideoConfig(),kind=scene.component;
  let visualStart=0;
  const cuts=(scene.visuals??[]).map((visual,index)=>{const from=visualStart,durationInFrames=scene.visualFrames[index];visualStart+=durationInFrames;return <Sequence key={index} from={from} durationInFrames={durationInFrames} name={`${scene.id} visual ${index+1}`}><VisualView scene={scene} media={media} placeholderMode={placeholderMode} visual={visual} visualFrames={durationInFrames} visualStart={from}/></Sequence>});
  const flash=isFirst?0:interpolate(frame,[0,6,12],[.4,.08,0],{extrapolateRight:'clamp'});
  const vo=media.voiceovers[scene.id];
  return <AbsoluteFill style={{background:NAVY,overflow:'hidden'}}>{cuts}{kind.includes('ScreenCapture')&&!kind.startsWith('ScreenCapture')&&frame>scene.durationInFrames*.65&&<AbsoluteFill style={{inset:'14% 12%',border:`3px solid ${AMBER}`,boxShadow:'0 20px 100px #000d'}}><Placeholder label="TRACKER SCREENSHOT / REAL RECEIPT PENDING"/></AbsoluteFill>}{isFirst&&frame<3*fps&&<AbsoluteFill><Placeholder label="OLIVER FACE FOOTAGE / FIRST 2–3 SECONDS"/></AbsoluteFill>}<AbsoluteFill style={{background:`linear-gradient(0deg, ${NAVY}dd 0%, transparent 48%)`,pointerEvents:'none'}}/>{!isFirst&&<ChapterCard scene={scene}/ >}{scene.on_screen_text&&scene.id!=='S8'&&<KineticType text={scene.on_screen_text} scene={scene}/ >}{isLast&&<TakeawayCards scene={scene}/ >}{isLast&&<EndCard scene={scene} content={endCard}/ >}{scene.manifest_slots?.map((slot,index)=>{const start=Math.round((slot.start??0)*fps),end=Math.round((slot.end??Math.min(scene.durationInFrames/fps,(slot.start??0)+5))*fps);return <Sequence key={index} from={start} durationInFrames={Math.max(1,end-start)}><div style={{position:'absolute',top:'68%',right:110,maxWidth:850,padding:'20px 30px',background:'#0a1628dd',borderTop:`3px solid ${CYAN}`,fontFamily:DATA,fontSize:23,color:PAPER}}>{slot.text??`${slot.type??'EVIDENCE'} SLOT · ${slot.asset??'MEDIA PENDING'}`}</div></Sequence>})}<FilmTexture/><AbsoluteFill style={{pointerEvents:'none',background:'#f5efe6',opacity:flash}}/>{vo&&<Audio src={staticFile(`vo/${vo.file}`)}/>}</AbsoluteFill>;
};

export const Documentary: React.FC<{manifest:VideoManifest;media:MediaInventory;timeline:{scenes:TimelineScene[];durationInFrames:number};placeholderMode:boolean}> = ({manifest,media,timeline,placeholderMode}) => <AbsoluteFill style={{background:NAVY}}>{timeline.scenes.map(scene=><Sequence key={scene.id} from={scene.fromFrame} durationInFrames={scene.durationInFrames} name={`${scene.id} ${scene.chapter}`}><SceneView scene={scene} media={media} placeholderMode={placeholderMode} isFirst={scene.fromFrame===0} isLast={scene.fromFrame+scene.durationInFrames===timeline.durationInFrames} endCard={manifest.end_card}/></Sequence>)}<div style={{display:'none'}}>{manifest.title}</div></AbsoluteFill>;
