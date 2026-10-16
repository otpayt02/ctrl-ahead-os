# CTRLAHEAD UI RULES

Cinematic interfaces for every UI. Strong UX first. Motion is the brand, not decoration.

Applies to every public frontend (`ai`, `piano`, `glass`) and the private OS dashboard.

## Non-negotiables

1. Every interactive element has a hover or focus state that eases in. No instant color jumps.
2. Every text reveal is cinematic: clip-path, mask, or staggered line/character reveal. Never a hard pop-in.
3. Scroll motion is driven by a Lenis smooth-scroll timeline. Pin, reveal, and color shifts are scrubbed or triggered from that timeline, not from unrelated scroll listeners.
4. Hover, focus, and scroll states share one easing language. Do not mix linear snaps with spring chaos on the same surface.
5. Reduced motion is required. `prefers-reduced-motion: reduce` disables parallax, character splits, and Lenis smoothing. Keep opacity and color fades under 200ms, or none.
6. Keyboard focus is visible and uses the same easing as hover. Never hide focus rings for aesthetics.
7. Motion never blocks reading, clicking, or form completion. If an animation is still running, the control must already be usable.

## Easing

| Token | Curve | Use |
| --- | --- | --- |
| `ease-cinematic` | `cubic-bezier(0.22, 1, 0.36, 1)` | Reveals, hovers, color, layout |
| `ease-exit` | `cubic-bezier(0.4, 0, 1, 1)` | Leave states only |
| `dur-micro` | 180–280ms | Buttons, links, chips, icons |
| `dur-reveal` | 700–1100ms | Headlines, section titles, hero lines |
| `dur-scene` | 1200–1800ms | Full-viewport scene changes |

Stagger text lines by 40–80ms. Never stagger more than 8 lines on one screen.

## Required micro-interactions

Every component below must implement at least one eased hover or focus effect, plus a scroll-timeline entrance if it appears below the fold.

- Nav links: underline grows from the left, color eases from muted to bone.
- Buttons: background color eases, slight lift (`translateY(-2px)`), no bounce.
- Cards: border or sheen eases in, image scale max 1.04 over 600ms.
- Headlines: line mask reveal on enter and on hover re-trigger only if the user re-enters the section.
- Body copy: fade + 12px rise, once, on Lenis timeline enter. No per-word hover on paragraphs.
- Inputs: border color and label position ease. Error states ease to amber, never flash red.
- Icons: stroke or fill eases. Rotate only for disclosure carets, max 180deg.
- Media frames: corner radius and overlay opacity ease. Play affordance fades in on hover.
- Tables and lists: row background eases. No row-height animation.
- Modals and drawers: backdrop opacity eases, panel slides 24px with `ease-cinematic`.

## Lenis timeline

- Initialize Lenis once at the app root. GSAP ScrollTrigger (or Motion One scroll) syncs to Lenis via `lenis.on('scroll', ScrollTrigger.update)`.
- One timeline per scene. Scenes are full sections, not individual buttons.
- Scrub only large scene changes (hero title, chapter markers, before/after). Hover states stay time-based, not scrubbed.
- Kill ScrollTrigger instances on route change. No leaked listeners.
- Mobile: same rules, shorter travel. No hover-only information. Touch focus states must match hover visually after tap.

## Color and type

- Background: near-black `#070708`. Text: bone `#f4efe6`. Accent: one per niche.
  - AI: electric amber `#e8a317`
  - Piano: cool ivory + ink `#d7d2c8` / `#101114`
  - Glass: furnace orange `#ff6a2a` on charcoal
- Hover color shifts stay inside the niche accent. Do not rainbow interactive states.
- Display type is tight, high contrast, and short. UI labels stay readable at 14px minimum.
- Do not use glassmorphism blur on text. Blur is for media frames only, max 12px.

## UX constraints

- One primary action per viewport.
- Loading states ease opacity. Never a layout jump when data arrives.
- Empty, error, and success states are designed, not browser defaults.
- All motion durations live in CSS variables or a shared motion token file. No magic numbers inside components.
- Do not autoplay sound. Piano and glass media start muted until the user presses play.

## Idea gate before video

A UI or content pass is not allowed to trigger render or edit until the creative-angle check passes:

1. The angle is specific to Oliver (builder, pianist, mechanic, church music, or glass), not a generic AI tip.
2. It shows a working artifact, a failure, or a measurable result.
3. It is not a duplicate of the last 5 shipped angles in `data/portfolio/`.
4. A reviewer can state the promise in one sentence.

If any check fails, stop. Do not render video. Revise the angle and re-run the gate.
