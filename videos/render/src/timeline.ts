import type {PacingConfig, VisualBeat} from './pacing';

export type ManifestScene = {
  id: string;
  chapter: string;
  start: number;
  end: number;
  assets?: string[];
  component: string;
  motion?: string;
  on_screen_text?: string;
  producer_note?: string;
  overlay_pool?: string[];
  visuals?: VisualBeat[];
  manifest_slots?: Array<{id?: string; start?: number; end?: number; text?: string; asset?: string; type?: string; recommended_animation?: string; annotation?: Record<string,string>; provenance?: Record<string,string>}>;
};

export type VideoManifest = {
  video_id: string;
  title: string;
  runtime_sec: number;
  fps: number;
  resolution: string;
  scenes: ManifestScene[];
  asset_prompts?: Record<string, string>;
  style?: {palette?: string[]; typefaces?: Record<string, string>; grade?: string};
  transitions?: string;
  pacing_sec?: number;
  pacing?: Partial<PacingConfig>;
  end_card?: {headline?: string; series?: string; teaser?: string};
};

export type MediaInventory = {
  videoId: string;
  availableAssets: string[];
  voiceovers: Record<string, {file: string; durationSeconds: number}>;
};

export type TimelineScene = ManifestScene & {
  fromFrame: number;
  durationInFrames: number;
  originalDurationInFrames: number;
  visualFrames: number[];
};

// Round cumulative boundaries, rather than every shot independently, so the last cut
// always ends on the chapter boundary even when VO stretches it.
export function visualFrameDurations(visuals: VisualBeat[], sceneFrames: number): number[] {
  if (!visuals.length) return [sceneFrames];
  const total = visuals.reduce((sum, visual) => sum + visual.duration_sec, 0);
  if (total <= 0 || sceneFrames < visuals.length) throw new Error('Invalid visual plan');
  let previous = 0;
  return visuals.map((visual, index) => {
    const elapsed = visuals.slice(0, index + 1).reduce((sum, item) => sum + item.duration_sec, 0);
    const boundary = index === visuals.length - 1 ? sceneFrames : Math.round(elapsed / total * sceneFrames);
    const frames = boundary - previous;
    if (frames < 1) throw new Error('Visual duration rounds below one frame');
    previous = boundary;
    return frames;
  });
}

export function buildTimeline(manifest: VideoManifest, media: MediaInventory) {
  if (!manifest.scenes.length) throw new Error('Manifest has no scenes');
  const [width, height] = manifest.resolution.split('x').map(Number);
  if (!width || !height || !manifest.fps) throw new Error('Invalid video dimensions or FPS');
  let frame = 0;
  const scenes: TimelineScene[] = manifest.scenes.map((scene, index) => {
    const originalFrames = Math.round((scene.end - scene.start) * manifest.fps);
    if (originalFrames < 1) throw new Error(`Invalid duration for ${scene.id}`);
    if (index > 0 && scene.start !== manifest.scenes[index - 1].end) {
      throw new Error(`Gap or overlap before ${scene.id}`);
    }
    const voSeconds = media.voiceovers[scene.id]?.durationSeconds ?? 0;
    const durationInFrames = Math.max(originalFrames, Math.ceil((voSeconds + (voSeconds ? 0.5 : 0)) * manifest.fps));
    const visualFrames = visualFrameDurations(scene.visuals ?? [], durationInFrames);
    const result = {...scene, fromFrame: frame, durationInFrames, originalDurationInFrames: originalFrames, visualFrames};
    frame += durationInFrames;
    return result;
  });
  if (manifest.scenes[0].start !== 0 || manifest.scenes[manifest.scenes.length - 1].end !== manifest.runtime_sec) {
    throw new Error('Scene bounds do not match manifest runtime');
  }
  return {scenes, durationInFrames: frame, width, height, fps: manifest.fps};
}
