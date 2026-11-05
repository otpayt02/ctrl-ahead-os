import {AbsoluteFill,Composition,OffthreadVideo,registerRoot,staticFile,useCurrentFrame} from 'remotion';
const gold='#e6bd69',green='#54e0a1';
const ramp=(f:number,s:number)=>{const u=Math.max(0,Math.min(1,(f-s)/12));return 1-(1-u)**4;};
export const Demo=()=>{
 const f=useCurrentFrame();
 const lines=[['Give your agent','a finish line.'],['Tell it what','done looks like.'],['Build. Check.','Fix what fails.'],['Define done.','Then let it build.']];
 const beat=Math.min(3,Math.floor(f/75));const p=ramp(f,beat*75);
 return <AbsoluteFill style={{background:'#080b12',color:'#f5efe5',fontFamily:'Arial,sans-serif',overflow:'hidden'}}>
 <div style={{position:'absolute',top:-130,left:0,width:1080,height:960,overflow:'hidden'}}><OffthreadVideo muted src={staticFile('overlay-base.mp4')} style={{width:1080,height:1920,position:'absolute',top:-230}}/></div>
 <div style={{position:'absolute',top:70,left:65,fontSize:27,fontWeight:800,letterSpacing:5,color:gold}}>AHEAD OF RUSH AI</div>
 <div style={{position:'absolute',top:805,left:45,right:45,height:850,background:'#151c29',border:'2px solid #354052',borderRadius:24,boxShadow:'0 25px 70px #000'}}>
 <div style={{height:70,padding:'22px 30px',boxSizing:'border-box',borderBottom:'1px solid #354052',fontSize:25,color:'#99a8bf'}}>● ● ●  BUILD BRIEF</div>
 <div style={{padding:35,fontSize:37,lineHeight:1.6}}><div style={{color:'#a2afc4',fontSize:26,letterSpacing:3}}>TASK</div><b>Build a file uploader.</b><div style={{marginTop:35,color:'#a2afc4',fontSize:26,letterSpacing:3}}>DONE WHEN</div>
 {['Choose a file','See upload progress','Recover from an error'].map((t,i)=><div key={t} style={{padding:'17px 10px',borderBottom:'1px solid #ffffff14',display:'flex',gap:20}}><span style={{color:f>150+i*20?green:'#65748a'}}>{f>150+i*20?'✓':'□'}</span>{t}</div>)}
 <div style={{marginTop:35,fontSize:30,color:green,opacity:ramp(f,215)}}>✓ All three checks complete</div></div></div>
 <div style={{position:'absolute',left:70,top:1055,width:936,height:360,border:`4px solid ${gold}`,borderRadius:18,opacity:ramp(f,68)*(1-ramp(f,150)),clipPath:`inset(0 ${100*(1-ramp(f,68))}% 0 0)`}}/>
 <svg width="1080" height="1920" style={{position:'absolute',opacity:ramp(f,90)*(1-ramp(f,150))}}><path d="M840 1530 C1020 1480 1030 1390 935 1340" fill="none" stroke={gold} strokeWidth="9" pathLength={1} strokeDasharray={1} strokeDashoffset={1-ramp(f,90)} strokeLinecap="round"/><path d="M940 1370 L929 1336 L965 1335" fill="none" stroke={gold} strokeWidth="9" strokeLinecap="round"/></svg>
 <div style={{position:'absolute',left:130,top:1470,fontSize:37,fontWeight:900,color:gold,opacity:ramp(f,90)*(1-ramp(f,150))}}>MAKE IT OBSERVABLE</div>
 <div style={{position:'absolute',top:650,left:35,right:35,textAlign:'center',fontSize:66,fontWeight:900,lineHeight:1.08,letterSpacing:-2,textShadow:'0 4px 12px #000',opacity:p,transform:`translateY(${25*(1-p)}px)`}}>{lines[beat][0]}<br/><span style={{color:gold}}>{lines[beat][1]}</span></div>
 <div style={{position:'absolute',bottom:135,left:70,right:70,fontSize:29,letterSpacing:3,color:'#9aa7bc'}}>WE DON’T CHASE THE FUTURE. WE CHECK IT.</div>
 <div style={{position:'absolute',bottom:95,left:70,height:4,width:940*f/299,background:gold}}/>
 </AbsoluteFill>;
};
registerRoot(()=> <Composition id="OverlayDemo" component={Demo} width={1080} height={1920} fps={30} durationInFrames={300}/>);
