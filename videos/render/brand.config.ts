import {Config} from '@remotion/cli/config';

Config.setEntryPoint('./src/brand/index.ts');
Config.setChromiumOpenGlRenderer('angle');
Config.setVideoImageFormat('png');
Config.setOverwriteOutput(true);
Config.setConcurrency(2);
