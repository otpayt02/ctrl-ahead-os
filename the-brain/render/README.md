# Render chain

`python build_manifest.py script.json remotion-template/sample-manifest.json` validates a sourced script and writes the scene manifest. The first scene must show a human face, last at most 3 seconds, and begin with a value-bearing hook. Each scene carries an image-generation prompt, narration, music cue, and optional on-screen text. Asset paths remain null until a human selects or creates rights-cleared media; the template displays placeholders rather than presenting prompts as actual footage.

In `remotion-template/`, run `npm install`, `npm run typecheck`, and `npm run studio` to inspect the composition. `npm run render` writes to `out/`. This is a scaffold; it does not synthesize narration, music, images, or a finished video.
