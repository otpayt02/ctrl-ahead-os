import {AbsoluteFill, Composition, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {SignalField} from './SignalField';
import {narrativeSeconds, phase, validateBrand, type BrandProps} from './motion';

const HEAD = 'M341 1182 C371 1110 359 1050 320 1001 C281 953 268 905 268 845 L268 730 C268 565 369 464 507 457 C646 450 739 537 747 674 C748 718 747 734 766 763 L821 840 Q838 862 806 871 L781 875 Q773 895 785 910 Q790 925 767 931 Q788 946 768 959 Q751 971 753 1001 C759 1063 724 1093 665 1088 L607 1082 Q580 1110 574 1206 C492 1166 420 1175 341 1182 Z';
const CLOUD = 'M350 865 C303 869 278 834 293 792 C267 758 283 712 322 703 C310 656 345 623 386 634 C399 587 454 571 492 600 C525 571 579 584 591 617 C644 596 687 626 687 667 C730 671 747 708 727 742 C756 778 735 824 702 831 C691 870 647 890 613 871 C583 899 541 888 522 870 C493 897 448 891 430 868 C397 890 364 885 350 865 Z';
const OUTPUT_PATH = 'M520 780 Q600 780 680 700 L930 450';

export const SignalBrand = (props: BrandProps) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = narrativeSeconds(frame, fps, props.durationSeconds);
  const {palette} = props;
  const headReveal = 0.12 + 0.88 * phase(t, 0, 1.25);
  const cloudReveal = phase(t, 0.30, 1.4);
  const arrowReveal = phase(t, 2.7, 4.35);
  const titleReveal = phase(t, 3.45, 4.55);
  const settle = phase(t, 4.3, 5.2);

  return <AbsoluteFill style={{backgroundColor: palette.background, overflow: 'hidden', fontFamily: 'Arial, Helvetica, sans-serif'}}>
    <AbsoluteFill style={{background: `radial-gradient(ellipse 600px 700px at 53% 43%, ${palette.purple}18, transparent 80%), radial-gradient(ellipse 500px 380px at 83% 24%, ${palette.emerald}09, transparent 80%)`}} />
    <svg viewBox="0 0 1080 1920" width={1080} height={1920} style={{position: 'absolute'}}>
      <defs>
        <linearGradient id="gold" x1="0" y1="1" x2="0.7" y2="0">
          <stop stopColor="#8e6834" /><stop offset="0.34" stopColor={palette.gold} /><stop offset="0.63" stopColor="#f8e0a0" /><stop offset="1" stopColor={palette.gold} />
        </linearGradient>
        <radialGradient id="cloud"><stop stopColor={palette.purple} stopOpacity="0.25" /><stop offset="1" stopColor={palette.purple} stopOpacity="0.04" /></radialGradient>
        <linearGradient id="output" x1="520" y1="780" x2="930" y2="450" gradientUnits="userSpaceOnUse">
          <stop stopColor={palette.emerald} stopOpacity="0" /><stop offset="0.24" stopColor={palette.emerald} /><stop offset="1" stopColor="#8aedb2" />
        </linearGradient>
      </defs>
      <g fill="none" stroke={palette.gold} strokeWidth="1" opacity="0.055">
        <circle cx="550" cy="790" r="430" /><circle cx="550" cy="790" r="470" />
        <path d="M100 790 H240 M865 790 H980 M550 290 V350 M550 1240 V1280" />
      </g>
      <path d={HEAD} fill={palette.background} fillOpacity="0.42" stroke={palette.gold} strokeWidth="6" opacity="0.12" />
      <path d={CLOUD} fill="url(#cloud)" opacity={cloudReveal} />
      <path d={CLOUD} fill="none" stroke={palette.purple} strokeWidth="18" opacity={cloudReveal * 0.07} />
      <path d={CLOUD} fill="none" stroke={palette.purple} strokeWidth="7" opacity={0.15 + cloudReveal * 0.85}
        pathLength={1} strokeDasharray={1} strokeDashoffset={1 - cloudReveal} strokeLinecap="round" />
      <g opacity={cloudReveal * (0.12 + settle * 0.1)} fill="none" stroke={palette.purple} strokeWidth="1.3">
        <path d="M400 693 Q470 650 541 694 T651 704 M386 820 Q469 837 513 817 T647 811" />
        <circle cx="400" cy="693" r="5" /><circle cx="541" cy="694" r="5" /><circle cx="647" cy="811" r="5" />
      </g>
    </svg>
    <SignalField seconds={t} settings={props} />
    <svg viewBox="0 0 1080 1920" width={1080} height={1920} style={{position: 'absolute'}}>
      <path d={HEAD} fill="none" stroke="url(#gold)" strokeWidth="7.5" pathLength={1}
        strokeDasharray={1} strokeDashoffset={1 - headReveal} strokeLinejoin="round" strokeLinecap="round" />
      <path d="M460 994 C478 1045 536 1063 607 1082" fill="none" stroke="url(#gold)" strokeWidth="5" opacity={phase(t, 0.8, 1.6)} />
      <path d={OUTPUT_PATH} fill="none" stroke={palette.emerald} strokeWidth="28" opacity={arrowReveal * 0.06}
        pathLength={1} strokeDasharray={1} strokeDashoffset={1 - arrowReveal} strokeLinecap="round" />
      <path d={OUTPUT_PATH} fill="none" stroke="url(#output)" strokeWidth="11" opacity={arrowReveal}
        pathLength={1} strokeDasharray={1} strokeDashoffset={1 - arrowReveal} strokeLinecap="round" />
      <path d="M930 450 L906 529 L885 495 L851 474 Z" fill={palette.emerald} opacity={phase(t, 4.05, 4.42)} />
    </svg>
    <div style={{position: 'absolute', top: 1330, left: 90, right: 90, textAlign: 'center', color: palette.gold}}>
      <div style={{overflow: 'hidden', height: 86}}>
        <div style={{fontSize: 65, lineHeight: '86px', fontWeight: 700, letterSpacing: 9,
          translate: `0 ${interpolate(titleReveal, [0, 1], [90, 0])}px`, opacity: titleReveal}}>AHEAD OF</div>
      </div>
      <div style={{overflow: 'hidden', height: 178}}>
        <div style={{fontSize: 172, lineHeight: '178px', letterSpacing: -7, fontWeight: 900, fontStyle: 'italic',
          translate: `0 ${interpolate(phase(t, 3.65, 4.7), [0, 1], [180, 0])}px`,
          backgroundImage: `linear-gradient(115deg, ${palette.gold}, #f9e5a7 48%, ${palette.gold})`, backgroundClip: 'text', color: 'transparent'}}>
          RUSH<span style={{fontSize: 48, fontStyle: 'normal', letterSpacing: 1, verticalAlign: 'top', marginLeft: 18, color: palette.purple}}>AI</span>
        </div>
      </div>
      <div style={{height: 2, width: 560, margin: '32px auto 34px', background: `linear-gradient(90deg, transparent, ${palette.gold}60, transparent)`, opacity: settle}} />
      <div style={{fontSize: 43, lineHeight: 1.4, fontWeight: 400, color: palette.ivory, opacity: phase(t, 4.35, 5.2), translate: `0 ${16 * (1 - settle)}px`}}>
        We don’t chase the future.<br /><span style={{color: palette.gold}}>We check it.</span>
      </div>
    </div>
  </AbsoluteFill>;
};

export const BrandRoot = () => <Composition
  id="AheadOfRushSignal" component={SignalBrand} width={1080} height={1920} fps={30} durationInFrames={180}
  defaultProps={{
    seed: 42, waveCount: 9, amplitudes: [44, 57, 36, 63, 41, 52, 32, 48, 38],
    convergenceIntervals: [[300, 555], [346, 610], [316, 580], [398, 650], [365, 622], [335, 600], [420, 670], [379, 640], [355, 615]],
    durationSeconds: 6, fps: 30,
    palette: {background: '#07090e', gold: '#e6bd69', purple: '#8253b9', emerald: '#45d990', ivory: '#f4efe6'},
  }}
  calculateMetadata={({props}) => {
    validateBrand(props);
    return {durationInFrames: Math.round(props.durationSeconds * props.fps), fps: props.fps};
  }}
/>;
