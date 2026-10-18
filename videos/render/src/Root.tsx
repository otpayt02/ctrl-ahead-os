import {Composition} from 'remotion';
import manifestJson from './generated-manifest.json';
import mediaJson from './generated-media.json';
import {Documentary} from './components';
import {buildTimeline, type MediaInventory, type VideoManifest} from './timeline';

const manifest = manifestJson as VideoManifest;
const media = mediaJson as MediaInventory;
const timeline = buildTimeline(manifest, media);

export const RemotionRoot: React.FC = () => <Composition
  id="LostCauseDraft"
  component={Documentary}
  durationInFrames={timeline.durationInFrames}
  fps={timeline.fps}
  width={timeline.width}
  height={timeline.height}
  defaultProps={{manifest, media, timeline, placeholderMode: false}}
/>;
