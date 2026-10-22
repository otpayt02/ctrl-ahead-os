import {BrowserAgents} from './BrowserAgents';
import {Composition} from 'remotion';
import manifestJson from './generated-manifest.json';
import mediaJson from './generated-media.json';
import {Documentary} from './components';
import {buildTimeline, type MediaInventory, type VideoManifest} from './timeline';
import {applyPacing} from './pacing';

const manifest = applyPacing(manifestJson as unknown as VideoManifest);
const media = mediaJson as MediaInventory;
const timeline = buildTimeline(manifest, media);

export const RemotionRoot: React.FC = () => <><Composition
  id="LostCauseDraft"
  component={Documentary}
  durationInFrames={timeline.durationInFrames}
  fps={timeline.fps}
  width={timeline.width}
  height={timeline.height}
  defaultProps={{manifest, media, timeline, placeholderMode: false}}
/><Composition id="BrowserAgentsShort" component={BrowserAgents} durationInFrames={1200} fps={30} width={1080} height={1920}/></>;
