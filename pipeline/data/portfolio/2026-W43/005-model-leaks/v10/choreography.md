# v10 choreography — Ctrl-Ahead 005 model leaks

## Rules enforced
- No slow zoompan anywhere. Motion cycles, in order, across every subsegment: pan-left, pan-right, slide-left (fast slide-in then hold), slide-right, crop top-left, crop bottom-right, pan-up, pan-down — so no two consecutive subsegments share a motion, and no image is slow-zoomed twice in a row.
- Every comma cut is a hard visual switch: a different crop region and, on alternating comma cuts, a different image from the rotation. No zoom pulse on the same frame.
- No two consecutive sentences share an image (rotation advances on a duplicate; the ledger image img48 is never used).
- Subtitles are the single-group karaoke system from v9 (tiktok9_fixed.ass, extended for the outro). Popups and outro overlays sit at the TOP of the frame; subtitles sit at the BOTTOM, so they never collide — this was frame-checked after an earlier build put them on top of each other.
- Proofs (sentences 15, 23, 24, 36, 41, 42, 43) use ONLY the dark gold-streak background with cinematic text fade-in, key phrases in gold, no document frame, no screenshot look, no border, and no words 'proof', 'manifest', 'ledger', or 'render' on screen. No ledger image appears anywhere.

## Per-sentence plan

### Sentence 0: One video title this week promised four huge model updates.
Witty read: Hook image: boxers — four names entering the ring, the fight the title promises.
Motion/image: pan-left
- 0.00-2.94: img00 (boxers), pan-left

### Sentence 1: GPT-7, Claude REA banned, Gemini Carbon insane, Qwen 4 leaks.
Witty read: LIST — each name gets its own stage: GPT-7 = moons (far-off, unreachable), Claude REA banned = empty stage (no such model exists to stand on it), Gemini Carbon = frosted glass (seen through, not usable), Qwen 4 leaks = tier cake (tiers stacked before anything ships). Gold popup per item, top of frame.
Motion/image: pan-right / slide-left / slide-right / crop-tl / crop-br / pan-up / pan-down
- 0.00-0.62: img15 (moons), pan-right, popup 'GPT-7'
- 0.62-2.32: img00 (boxers), slide-left
- 2.32-2.72: img21 (empty-stage), slide-right, popup 'Claude REA banned'
- 2.72-3.98: img00 (boxers), crop-tl
- 3.98-5.44: img34 (frosted), crop-br, popup 'Gemini Carbon'
- 5.44-6.92: img41 (tier-cake), pan-up, popup 'Qwen 4 leaks'
- 6.92-7.56: img00 (boxers), pan-down

### Sentence 2: I checked all four against what the companies actually said.
Motion/image: pan-left
- 0.00-3.28: img01 (posters), pan-left

### Sentence 3: One is a rumor, one I could not find at all, one is a leak with no product, and one is real but not shipped.
Witty read: LIST — verdicts as evidence, not adjectives: rumor = anonymous envelope, could not find it = empty folder, leak with no product = frosted glass, real not shipped = treadmill (moving, going nowhere yet).
Motion/image: pan-right / slide-left / slide-right / crop-tl / crop-br / pan-up / pan-down
- 0.00-0.52: img10 (envelope), pan-right, popup 'a rumor'
- 0.52-1.08: img01 (posters), slide-left
- 1.08-2.52: img12 (empty-folder), slide-right, popup 'could not find it'
- 2.52-2.90: img01 (posters), crop-tl
- 2.90-4.36: img34 (frosted), crop-br, popup 'a leak, no product'
- 4.36-4.74: img01 (posters), pan-up
- 4.74-6.04: img40 (treadmill), pan-down, popup 'real, not shipped'

### Sentence 4: Here is the scorecard, so you do not build on a rumor.
Motion/image: pan-left / pan-right
- 0.00-1.98: img02 (detective), pan-left
- 1.98-4.36: img04 (scorecard), pan-right

### Sentence 5: Before the evidence, here is the thought I want you to carry through all four.
Motion/image: slide-left / slide-right
- 0.00-0.76: img03 (doors), slide-left
- 0.76-3.40: img05 (mirror), slide-right

### Sentence 6: A rumor is not just a bad fact.
Witty read: A rumor is a mirror — literally the mirror image. The visual is the argument, not decoration.
Motion/image: crop-tl
- 0.00-2.94: img06 (trophy-mirror), crop-tl

### Sentence 7: It is a mirror.
Witty read: Trophy in a mirror — wanting the win to be true is the distortion, not the trophy itself.
Motion/image: crop-br
- 0.00-1.22: img07 (certainty), crop-br

### Sentence 8: It shows you what you already wanted to be true.
Witty read: Certainty bottles — what the title is really selling when it promises the next giant model.
Motion/image: pan-up
- 0.00-2.94: img08 (scale), pan-up

### Sentence 9: When a title promises the next giant model, the next ban, the next leak, it is not only selling news, it is selling cert
Witty read: A scale — hype on one side, what was actually said on the other.
Motion/image: pan-down / pan-left / pan-right / slide-left / slide-right
- 0.00-2.10: img09 (hourglass), pan-down
- 2.10-3.14: img11 (paperplane), pan-left
- 3.14-3.98: img13 (label-jar), pan-right
- 3.98-6.00: img15 (moons), slide-left
- 6.00-9.94: img17 (locked-door), slide-right

### Sentence 10: The directive is simple, and it is hard: want the truth more than you want the headline.
Motion/image: crop-tl / crop-br
- 0.00-1.04: img06 (trophy-mirror), crop-tl
- 1.04-5.28: img08 (scale), crop-br

### Sentence 11: If you can hold that for six minutes, the rest of this video will feel less like a debunk and more like a discipline.
Motion/image: pan-up / pan-down
- 0.00-1.58: img07 (certainty), pan-up
- 1.58-5.74: img09 (hourglass), pan-down

### Sentence 12: First, GPT-7 Bel.
Motion/image: pan-left / pan-right
- 0.00-0.86: img07 (certainty), pan-left
- 0.86-2.82: img09 (hourglass), pan-right

### Sentence 13: The whole thing traces to one anonymous post on August 25th.
Witty read: Anonymous post — an envelope with no sender. That is the whole evidence base for Bel.
Motion/image: slide-left
- 0.00-2.44: img10 (envelope), slide-left

### Sentence 14: No document, no named source, and it did not even say GPT-7 — that label came later.
Witty read: LIST — no document = empty folder, no named source = envelope with no sender, did not say GPT-7 = crossed-out label. Absence shown as absence, not as a scary graphic.
Motion/image: slide-right / crop-tl / crop-br / pan-up / pan-down / pan-left
- 0.00-1.25: img12 (empty-folder), slide-right, popup 'no document'
- 1.25-2.20: img12 (empty-folder), crop-tl
- 2.20-3.02: img10 (envelope), crop-br, popup 'no named source'
- 3.02-3.32: img12 (empty-folder), pan-up
- 3.32-4.51: img16 (crossed), pan-down, popup 'did not say GPT-7'
- 4.51-7.56: img12 (empty-folder), pan-left

### Sentence 15: OpenAI has never used the name Bel in public, and on October 11th its own models
Witty read: PROOF REPLACEMENT — no screenshot, no card. Gold-streak background, text fades in line by line: GPT-6 Astra, GPT-6.1 Sol, GPT-6 Luna, no Bel. The models page is the point; the page itself is never shown as a document.
Motion/image: proof-cinematic-reveal (gold-streak bg, text fade-in, no screenshot, no card)
- proof lines: ['GPT-6 Astra', 'GPT-6.1 Sol', 'GPT-6 Luna', 'no Bel']

### Sentence 16: No Bel, no GPT-7.
Motion/image: slide-left
- 0.00-2.36: img10 (envelope), slide-left

### Sentence 17: What OpenAI did say, on September 8th, is that it has an internal model significantly more capable than GPT-6 Astra.
Motion/image: slide-right / crop-tl / crop-br
- 0.00-1.38: img11 (paperplane), slide-right
- 1.38-2.78: img13 (label-jar), crop-tl
- 2.78-7.74: img15 (moons), crop-br

### Sentence 18: That is true, and it is not the same as saying that model is Bel, or that it is GPT-7.
Motion/image: pan-up / pan-down / pan-left
- 0.00-0.84: img11 (paperplane), pan-up
- 0.84-3.37: img13 (label-jar), pan-down
- 3.37-6.02: img15 (moons), pan-left

### Sentence 19: Verdict: unverified.
Motion/image: pan-right
- 0.00-2.38: img12 (empty-folder), pan-right

### Sentence 20: Second, Claude REA banned.
Motion/image: slide-left
- 0.00-1.76: img13 (label-jar), slide-left

### Sentence 21: I searched for a model called Claude REA, and I did not find one.
Witty read: Empty stage — searched for a model called Claude REA, found no one standing there.
Motion/image: slide-right / crop-tl
- 0.00-1.61: img21 (empty-stage), slide-right
- 1.61-3.58: img23 (calendar), crop-tl

### Sentence 22: What I did find is two real bans, and neither is a model.
Witty read: Two stamps — two real bans, neither a model. Stamps, not a courtroom, because these are account/policy actions.
Motion/image: crop-br / pan-up
- 0.00-1.51: img22 (two-stamps), crop-br
- 1.51-3.50: img24 (heart-bubble), pan-up

### Sentence 23: On October 8th, Anthropic updated its usage policy, effective November 12th, to 
Motion/image: proof-cinematic-reveal (gold-streak bg, text fade-in, no screenshot, no card)
- proof lines: ['sustained, needless cruelty', 'toward Claude']

### Sentence 24: And on October 12th, Anthropic said it banned tens of thousands of accounts for 
Motion/image: proof-cinematic-reveal (gold-streak bg, text fade-in, no screenshot, no card)
- proof lines: ['tens of thousands of accounts banned', 'for distillation']

### Sentence 25: So banned is real, but it is accounts and a policy, not a model called REA.
Motion/image: pan-right / slide-left / slide-right
- 0.00-1.06: img16 (crossed), pan-right
- 1.06-2.90: img18 (two-doors), slide-left
- 2.90-4.98: img20 (searchbar), slide-right

### Sentence 26: Pause on that word, banned, because it is doing philosophical work here, not just legal work.
Motion/image: crop-tl / crop-br / pan-up
- 0.00-0.84: img17 (locked-door), crop-tl
- 0.84-3.58: img19 (stamp), crop-br
- 3.58-5.24: img21 (empty-stage), pan-up

### Sentence 27: To ban an account is to draw a boundary around a community.
Witty read: A fence — to ban an account is to draw a boundary around a community, so the image is a boundary, not a punishment.
Motion/image: pan-down
- 0.00-3.38: img29 (fence), pan-down

### Sentence 28: To ban a behavior is to say, this is not how we will treat a mind, even a simulated one.
Witty read: Heart in a bubble — to ban a behavior is a claim about how a mind, even a simulated one, should be treated.
Motion/image: pan-left / pan-right / slide-left
- 0.00-1.60: img24 (heart-bubble), pan-left
- 1.60-3.72: img26 (copy-machine), pan-right
- 3.72-5.84: img28 (pause), slide-left

### Sentence 29: To ban a model would be something else entirely: to erase a capability from the world.
Witty read: Vanishing figure — to ban a model would be erasing a capability from the world, so the image disappears instead of being struck down.
Motion/image: slide-right
- 0.00-5.24: img38 (vanishing), slide-right

### Sentence 30: The title collapses all three into one scary word, and that collapse is the trick.
Motion/image: crop-tl / crop-br
- 0.00-3.04: img19 (stamp), crop-tl
- 3.04-5.36: img21 (empty-stage), crop-br

### Sentence 31: When you hear a word that big, ask what exactly was banned, by whom, and from whom.
Motion/image: pan-up / pan-down / pan-left / pan-right
- 0.00-1.44: img20 (searchbar), pan-up
- 1.44-3.38: img22 (two-stamps), pan-down
- 3.38-4.14: img24 (heart-bubble), pan-left
- 4.14-5.82: img26 (copy-machine), pan-right

### Sentence 32: Precision is not pedantry here.
Motion/image: slide-left
- 0.00-2.12: img21 (empty-stage), slide-left

### Sentence 33: Precision is the difference between fear and understanding.
Motion/image: slide-right
- 0.00-3.34: img22 (two-stamps), slide-right

### Sentence 34: Third, Gemini 4 Carbon.
Motion/image: crop-tl / crop-br
- 0.00-0.40: img23 (calendar), crop-tl
- 0.40-1.70: img25 (door-closing), crop-br

### Sentence 35: This one is the closest to real, and it is still not a product.
Witty read: Frosted glass — Carbon is the closest to real and still not a product: visible through glass, not in your hands.
Motion/image: pan-up / pan-down
- 0.00-2.04: img34 (frosted), pan-up
- 2.04-4.38: img36 (cloud-ruler), pan-down

### Sentence 36: Business Insider reported on October 9th that Google staff were testing Carbon i
Witty read: PROOF REPLACEMENT — gold-streak background, text only: Carbon tested inside Google; no model card, no price, no date; not confirmed.
Motion/image: proof-cinematic-reveal (gold-streak bg, text fade-in, no screenshot, no card)
- proof lines: ['Carbon tested inside Google', 'no model card, no price, no date', 'not confirmed']

### Sentence 37: Feels like is not a benchmark, there is no model card, no price, no release date, and Google has not confirmed it.
Witty read: LIST — no model card = empty folder, no price = label jar with no price on it, no release date = calendar with no date circled, not confirmed = crossed-out claim.
Motion/image: pan-right / slide-left / slide-right / crop-tl / crop-br / pan-up / pan-down / pan-left / pan-right
- 0.00-2.02: img24 (heart-bubble), pan-right
- 2.02-2.94: img12 (empty-folder), slide-left, popup 'no model card'
- 2.94-3.08: img24 (heart-bubble), slide-right
- 3.08-3.76: img13 (label-jar), crop-tl, popup 'no price'
- 3.76-3.88: img24 (heart-bubble), crop-br
- 3.88-4.70: img23 (calendar), pan-up, popup 'no release date'
- 4.70-4.94: img24 (heart-bubble), pan-down
- 4.94-6.32: img16 (crossed), pan-left, popup 'not confirmed'
- 6.32-7.06: img24 (heart-bubble), pan-right

### Sentence 38: A checkpoint briefly showed up on LMArena around October 23rd and was pulled.
Motion/image: slide-left
- 0.00-4.32: img25 (door-closing), slide-left

### Sentence 39: So Carbon is a leak about an internal checkpoint, not a model you can use today.
Motion/image: slide-right / crop-tl
- 0.00-2.96: img26 (copy-machine), slide-right
- 2.96-5.64: img28 (pause), crop-tl

### Sentence 40: Fourth, Qwen 4.
Motion/image: crop-br
- 0.00-1.68: img41 (tier-cake), crop-br

### Sentence 41: Alibaba said on September 22nd that Qwen 4 is in training.
Witty read: PROOF REPLACEMENT — gold-streak background, text only: Qwen 4 in training; no specs, no date.
Motion/image: proof-cinematic-reveal (gold-streak bg, text fade-in, no screenshot, no card)
- proof lines: ['Qwen 4 in training', 'no specs, no date']

### Sentence 42: It named tiers — Max, Plus, Flash, and a 27B model — but gave no specs, no date,
Witty read: PROOF REPLACEMENT + LIST — gold-streak background, text only: Max, Plus, Flash, 27B; no specs, no date; no Qwen 4 weights on Hugging Face.
Motion/image: proof-cinematic-reveal (gold-streak bg, text fade-in, no screenshot, no card)
- proof lines: ['Max, Plus, Flash, 27B', 'no specs, no date', 'no Qwen 4 weights on Hugging Face']

### Sentence 43: The thing you can actually look at today is Qwen 3.8 Flash-Next, which Alibaba i
Witty read: PROOF REPLACEMENT — gold-streak background, text only: Qwen 3.8 Flash-Next; no Qwen 4 weights on Hugging Face.
Motion/image: proof-cinematic-reveal (gold-streak bg, text fade-in, no screenshot, no card)
- proof lines: ['Qwen 3.8 Flash-Next', 'no Qwen 4 weights on Hugging Face']

### Sentence 44: So Qwen 4 is real as a project, not shipped as a model.
Motion/image: pan-right / slide-left
- 0.00-1.96: img37 (empty-shelf), pan-right
- 1.96-3.92: img39 (locked-app), slide-left

### Sentence 45: And Qwen 4 Coder does not exist yet.
Witty read: Empty chair — Qwen 4 Coder does not exist yet, so the chair for it is empty. Not a missing person, a missing product.
Motion/image: slide-right
- 0.00-2.76: img44 (empty-chair), slide-right

### Sentence 46: A leak is a model before it has a name, a price, or a promise.
Motion/image: crop-tl / crop-br / pan-up
- 0.00-1.96: img30 (handshake), crop-tl
- 1.96-2.62: img32 (questions), crop-br
- 2.62-4.16: img34 (frosted), pan-up

### Sentence 47: It lives in the gap between what a lab knows and what the public is allowed to know, and that gap is where imagination r
Witty read: Canyon bridge — a leak lives in the gap between what a lab knows and what the public is allowed to know; the bridge is the gap itself.
Motion/image: pan-down / pan-left
- 0.00-4.18: img45 (canyon-bridge), pan-down
- 4.18-7.92: img47 (bricks), pan-left

### Sentence 48: That is not a flaw in you.
Motion/image: pan-right
- 0.00-1.86: img31 (eraser), pan-right

### Sentence 49: It is how humans think about power we cannot yet touch.
Motion/image: slide-left
- 0.00-2.90: img32 (questions), slide-left

### Sentence 50: We fill the unknown with the biggest thing we can picture.
Motion/image: slide-right
- 0.00-3.92: img33 (fog-clearing), slide-right

### Sentence 51: The discipline is to let the unknown stay unknown for a little longer.
Motion/image: crop-tl
- 0.00-4.08: img34 (frosted), crop-tl

### Sentence 52: A checkpoint is not a product.
Witty read: Not-equal sign — a checkpoint is not a product, stated as an equation that does not balance.
Motion/image: crop-br
- 0.00-1.86: img46 (not-equal), crop-br

### Sentence 53: A feeling is not a benchmark.
Motion/image: pan-up
- 0.00-2.06: img35 (lab-bench), pan-up

### Sentence 54: A training run is not a release.
Witty read: Treadmill — a training run is not a release: motion without arrival.
Motion/image: pan-down
- 0.00-1.22: img40 (treadmill), pan-down

### Sentence 55: Naming each stage honestly is how you keep your own thinking clean.
Motion/image: pan-left
- 0.00-5.16: img36 (cloud-ruler), pan-left

### Sentence 56: So if you are picking a model this week, pick from the ones that actually shipped: GPT-6 Astra, Claude Opus 5.5, Gemini 
Witty read: LIST — only shipped models get a stage: GPT-6 Astra = scorecard, Claude Opus 5.5 = trophy mirror, Gemini 4 Argon = moons (limited form, still distant), Qwen 3.8 = poster (a preview you can actually look at).
Motion/image: pan-right / slide-left / slide-right / crop-tl / crop-br / pan-up / pan-down / pan-left
- 0.00-3.82: img37 (empty-shelf), pan-right
- 3.82-5.62: img04 (scorecard), slide-left, popup 'GPT-6 Astra'
- 5.62-5.90: img37 (empty-shelf), slide-right
- 5.90-6.51: img06 (trophy-mirror), crop-tl, popup 'Claude Opus 5.5'
- 6.51-7.86: img37 (empty-shelf), crop-br
- 7.86-10.08: img15 (moons), pan-up, popup 'Gemini 4 Argon'
- 10.08-10.18: img43 (poster), pan-down, popup 'Qwen 3.8'
- 10.18-11.98: img37 (empty-shelf), pan-left

### Sentence 57: The other four names are a rumor, a missing model, a leak, and a training run.
Witty read: LIST — the other four names, each in its own image again: rumor = envelope, missing model = empty stage, leak = frosted glass, training run = treadmill.
Motion/image: pan-right / slide-left / slide-right / crop-tl / crop-br / pan-up / pan-down / pan-left / pan-right
- 0.00-1.08: img37 (empty-shelf), pan-right
- 1.08-1.51: img10 (envelope), slide-left, popup 'a rumor'
- 1.51-1.84: img37 (empty-shelf), slide-right
- 1.84-2.54: img21 (empty-stage), crop-tl, popup 'a missing model'
- 2.54-2.76: img37 (empty-shelf), crop-br
- 2.76-3.12: img34 (frosted), pan-up, popup 'a leak'
- 3.12-3.46: img37 (empty-shelf), pan-down
- 3.46-4.20: img40 (treadmill), pan-left, popup 'a training run'
- 4.20-4.76: img37 (empty-shelf), pan-right

### Sentence 58: That is not less interesting — it is just the difference between news and hype, and that difference is the whole point.
Motion/image: slide-left / slide-right
- 0.00-4.02: img38 (vanishing), slide-left
- 4.02-6.44: img40 (treadmill), slide-right

### Sentence 59: One last test before you share anything this week.
Motion/image: crop-tl
- 0.00-2.70: img39 (locked-app), crop-tl

### Sentence 60: Ask who benefits if you believe it now, before it is confirmed.
Motion/image: crop-br / pan-up
- 0.00-1.76: img40 (treadmill), crop-br
- 1.76-3.44: img42 (empty-library), pan-up

### Sentence 61: If the answer is a channel selling urgency, a seller selling access, or your own desire to be first, slow down.
Witty read: LIST — who benefits, each shown as a motive: channel selling urgency = posters, seller selling access = label jar, own desire to be first = mirror. The third one is the point — it implicates the viewer, not just the sellers.
Motion/image: pan-down / pan-left / pan-right / slide-left / slide-right / crop-tl / crop-br
- 0.00-0.64: img40 (treadmill), pan-down
- 0.64-1.78: img01 (posters), pan-left, popup 'channel selling urgency'
- 1.78-2.26: img40 (treadmill), pan-right
- 2.26-3.44: img13 (label-jar), slide-left, popup 'seller selling access'
- 3.44-3.84: img40 (treadmill), slide-right
- 3.84-5.19: img05 (mirror), crop-tl, popup 'own desire to be first'
- 5.19-7.16: img40 (treadmill), crop-br

### Sentence 62: Speed is not insight.
Motion/image: pan-up
- 0.00-1.72: img41 (tier-cake), pan-up

### Sentence 63: Being first to repeat a rumor is not the same as being right, and in a field that moves this fast, the person who waits 
Motion/image: pan-down / pan-left / pan-right
- 0.00-2.88: img42 (empty-library), pan-down
- 2.88-4.84: img44 (empty-chair), pan-left
- 4.84-8.34: img46 (not-equal), pan-right

### Sentence 64: They are the only one still standing on solid ground when the hype cycle turns.
Motion/image: slide-left
- 0.00-4.20: img42 (empty-library), slide-left

### Sentence 65: And here is the directive I want you to leave with.
Motion/image: slide-right
- 0.00-2.58: img43 (poster), slide-right

### Sentence 66: Build on what shipped.
Motion/image: crop-tl
- 0.00-1.68: img44 (empty-chair), crop-tl

### Sentence 67: Watch what is rumored, but do not bet your work, your money, or your reputation on it.
Motion/image: crop-br / pan-up / pan-down / pan-left
- 0.00-0.88: img45 (canyon-bridge), crop-br
- 0.88-2.40: img47 (bricks), pan-up
- 2.40-3.12: img00 (boxers), pan-down
- 3.12-4.42: img02 (detective), pan-left

### Sentence 68: Keep a ledger, even a mental one: claimed, sourced, confirmed, shipped.
Witty read: LIST — claimed = envelope, sourced = detective, confirmed = scorecard, shipped = bricks. The last image is deliberately bricks, not a ledger document: building on what shipped, one brick at a time, and no ledger/render-manifest image appears anywhere in this video.
Motion/image: pan-right / slide-left / slide-right / crop-tl / crop-br / pan-up / pan-down / pan-left / pan-right
- 0.00-2.98: img47 (bricks), pan-right
- 2.98-3.32: img10 (envelope), slide-left, popup 'claimed'
- 3.32-4.12: img47 (bricks), slide-right
- 4.12-4.17: img02 (detective), crop-tl, popup 'sourced'
- 4.17-4.78: img47 (bricks), crop-br
- 4.78-4.83: img04 (scorecard), pan-up, popup 'confirmed'
- 4.83-5.42: img47 (bricks), pan-down
- 5.42-5.47: img47 (bricks), pan-left, popup 'shipped'
- 5.47-6.12: img47 (bricks), pan-right

### Sentence 69: Four columns.
Motion/image: slide-left
- 0.00-1.24: img45 (canyon-bridge), slide-left

### Sentence 70: Most of the internet lives in the first two.
Motion/image: slide-right
- 0.00-2.34: img46 (not-equal), slide-right

### Sentence 71: Your advantage is living in the last two.
Motion/image: crop-tl
- 0.00-2.32: img47 (bricks), crop-tl

### Sentence 72: That is not cynicism.
Motion/image: crop-br
- 0.00-1.48: img47 (bricks), crop-br

### Sentence 73: That is stewardship.
Motion/image: pan-up
- 0.00-1.56: img47 (bricks), pan-up

### Sentence 74: The future will arrive whether you hype it or not, and when it does, you will be ready for it precisely because you did 
Witty read: Canyon bridge again, now as the future arriving — the bridge is crossed, not hyped.
Motion/image: pan-down / pan-left / pan-right
- 0.00-2.20: img45 (canyon-bridge), pan-down
- 2.20-3.18: img47 (bricks), pan-left
- 3.18-7.65: img00 (boxers), pan-right

## Outro (after 351.888s main, 0.5s black fade, then 25.92s outro voiceover)
- Beat 1 (0-12s of outro): brass arrow image, pan-left. Welcome: first video, you are early.
- Beat 2 (12-19s): brass arrow, slide-right, big gold SUBSCRIBE popup at the top of the frame (drawbox + text, not a YouTube screenshot).
- Beat 3 (19-23.5s): brass arrow, crop top-left, catchphrase at the top: 'We don't chase the future. We check it.' (second line in gold).
- Beat 4 (23.5-25.92s): brass arrow, pan-down, final brand line at the top: 'Ctrl-Ahead — confirmed, not just claimed.' The brass arrow is the small brand mark to remember the channel by.

## Known limits
- Subtitle/visual drift: each segment is rendered to whole frames at 30fps, so the video track runs 0.96s longer than the 378.308s audio track (video 379.267s, audio 378.308s, silent hold on the final brand frame). Visual/subtitle alignment can drift by up to ~1s by the end of the video.
- Proof text reveals are line-by-line fade-ins, not word-by-word, because the cited phrases are not the spoken narration words.
- List item timings use the (often duplicated) Whisper word times, clamped to be monotonic, so a popup may start a fraction of a second before or after the spoken item in fast lists.