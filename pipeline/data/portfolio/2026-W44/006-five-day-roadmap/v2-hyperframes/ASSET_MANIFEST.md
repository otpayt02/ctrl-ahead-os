# Asset manifest — 006 v2 (HyperFrames + GSAP)

Provenance lives here and in BUILD_NOTES.md only — never on any video frame.
All media below was generated 2026-10-30 with the built-in media generation tools
(media.generate_image / media.generate_video), in the channel grade: cinematic digital
illustration, deep charcoal-navy, neon cyan + neon pink accents, warm brass-gold
highlights, no text/logos/watermarks, illustrated metaphor only — never presented as
real screenshots, recordings, dashboards, or evidence.

## Generated video clips (6) — metaphor/atmosphere only
| File | Used in | Content |
|---|---|---|
| assets/gen/vid-hook-1-deploy.mp4 | s01 hook 0.0–6.6s | Terminal deploy, checks flipping green |
| assets/gen/vid-hook-2-app.mp4 | s01 hook 6.6–13.1s | Web app interface assembling itself |
| assets/gen/vid-hook-3-dashboards.mp4 | s01 hook 13.1–19.7s | Dashboard wall lighting up |
| assets/gen/vid-s03-3-docker.mp4 | s03_3 Docker 0–10s | Glowing app-box on turntable |
| assets/gen/vid-s05-1-lambda.mp4 | s05_1 Lambda 0–10s | Motion-sensor porch light + brass meter + walker (photoreal clip) |
| assets/gen/vid-s07-1-deploy.mp4 | s07_1 Deploy 0–10s | Launch wall flipping amber → green |

Clips are 1280×720, 10s each, used once each, muted, trimmed by scene timing.
Each clip segment crossfades to its generated still (below) for the remainder of
the segment — no clip or image is reused anywhere else in the film.

## Generated images (18) — one per segment, used once
| File | Segment |
|---|---|
| assets/gen/img-s01-hook-desk.webp | s01 hook (closing beat) — developer desk, green status lights |
| assets/gen/img-s02-intro.webp | s02 — planning wall, five card slots, brass route line |
| assets/gen/img-s03-1-git.webp | s03_1 Git — checkpoint portal trail (time machine) |
| assets/gen/img-s03-2-aws.webp | s03_2 AWS Account — brass utility meter on a cloud |
| assets/gen/img-s03-3-docker.webp | s03_3 Docker — app packed in a glowing box |
| assets/gen/img-s03-4-cursor.webp | s03_4 Cursor + Claude — ghost typist at a glowing editor |
| assets/gen/img-s03-5-amplify.webp | s03_5 Amplify — printing press stamping site copies |
| assets/gen/img-s03-6-sam.webp | s03_6 SAM — blueprint rising into a 3D backend diagram |
| assets/gen/img-s04-1-react.webp | s04_1 React — interface bricks snapping together |
| assets/gen/img-s04-2-vibe.webp | s04_2 Vibe Coding — finished facade, empty scaffolding behind |
| assets/gen/img-s04-3-gateway.webp | s04_3 API Gateway — grand front door, checker + queue |
| assets/gen/img-s05-1-lambda.webp | s05_1 Lambda — motion-sensor lamp (after clip) |
| assets/gen/img-s05-2-aibuild.webp | s05_2 AI Backend Build — stamping service tickets |
| assets/gen/img-s05-3-queue.webp | s05_3 FastAPI + SQS — ticket dispenser + queue |
| assets/gen/img-s06-1-dynamo.webp | s06_1 DynamoDB — glowing filing cabinet |
| assets/gen/img-s06-2-testing.webp | s06_2 Testing — two machine halves wired across a seam |
| assets/gen/img-s06-3-garage.webp | s06_3 RDS + S3 — infinite glowing garage shelves |
| assets/gen/img-s07-1-deploy.webp | s07_1 Deploy — launch wall (after clip) |
| assets/gen/img-s07-2-cloudwatch.webp | s07_2 CloudWatch — heart-monitor trace + camera wall |
| assets/gen/img-s07-3-gauges.webp | s07_3 Grafana + X-Ray — gauges wall + package route |
| assets/gen/img-s08-route.webp | s08 Close — five-stop route map, final node brightest |
| assets/gen/img-outro-arrow.webp | Outro — brass arrow brand mark |

(That is 21 segment images + the outro mark = 22 rows counting s01; generation
batches: 18 image-generation calls total, several segments share a row above with
their clip counterparts.)

## Audio
- assets/audio/final-mix.m4a — the exact v1 final mix (Helio VO verbatim with the
  two fact fixes, synthesized music bed, chip ticks, day-card stingers), extracted
  from the v1 master. v2 keeps the identical timeline (495.93s), so VO, ticks and
  captions stay in sync. No new VO was recorded for v2.

## Animation (all GSAP, in-composition)
- Pill segment label slides in; name card + gold underline draw; per-beat headline
  swaps with underline sweep at every chip trigger; WHAT/WHY/SKIP/HOW chips stamp
  in (back.out) at Whisper-aligned trigger words; Git checkpoint nodes light in
  sequence; LATER segments get a muted overlay + rotated LATER badge; day cards
  slam with a gradient rule draw; captions are single-line, script-spoken words
  turning gold at their word timestamps; outro arrow scales in with catchphrase,
  tagline and a SUBSCRIBE pill pop.
- No slow zoom anywhere; no image, clip, or motion repeated.
