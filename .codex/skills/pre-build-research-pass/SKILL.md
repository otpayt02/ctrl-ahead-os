---
name: pre-build-research-pass
description: Final exhaustive research/sanity-check sweep immediately before committing to a build phase. Mines official docs, peer-reviewed databases, industry benchmarks, community data, and open datasets for anything that would materially change the plan. Use when the user says "last ditch", "sanity check", "before we build", "final pass", or before any phase transition in ROADMAP.md.
---

# Pre-Build Research Pass (Last-Ditch Sanity Check)

## Purpose
One structured sweep right before build starts: find anything that would change the design, save it, then stop researching and build.

## Procedure — run all 6 lanes
1. **Official / first-party.** Platform docs, official blogs, API references, changelogs. Note exact metric names, availability, and API access (or lack of it).
2. **Peer-reviewed.** EBSCOhost, Google Scholar, arXiv, ACM, PubMed. 3-5 Boolean-themed queries. Extract findings, sample sizes, confidence.
3. **Industry benchmarks.** Reputable analytics firms, data-backed tool blogs, platform creator-insider statements.
4. **Community / creator-backed.** High-signal creator reports, verified experiments, large-sample forum posts. Label confidence lower than peer-reviewed.
5. **Open data / datasets / leaks.** Public datasets, published API dumps, documented limitations. Never scrape private analytics or violate ToS — note when data is owner-only.
6. **Contradiction check.** Explicitly list what the evidence disputes about the current plan.

## Output contract (numbered task block)
For each lane: sources found (count), top findings (source + type), confidence (high/med/low), and impact on build — CHANGE / CONFIRM / IGNORE with a one-line reason.

## Hard limits
- All 6 lanes get at least one check or a documented "no data found" — then the pass ends.
- Cap ~10 sources per lane; quality over volume.
- Every claim gets a source or is labeled UNVERIFIED.
- End with a go/no-go verdict and a delta list: exactly what changed in the plan because of this pass.

## Integration
- Save findings to `<project>/research/<topic>.md`, commit with `research:` prefix, push.
- Update ROADMAP.md if findings change sequencing.
- Fold adopted tactics into the relevant prompts (e.g., `yt-niche-intel/prompts.md`).