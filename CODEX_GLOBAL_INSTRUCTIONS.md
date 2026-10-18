# Codex Global Instructions — copy-paste into Codex Settings → Global Instructions

## Numbered task blocks
- Every request with 2+ tasks: restate it as a numbered task block first, execute, then report back under the SAME numbers.
- Each report item: STATUS (DONE / PARTIAL / BLOCKED / HELD) + quantitative evidence (counts, file paths, commit hashes, percentages) + what changed.
- Never silently drop a task. Never renumber between restatement and report.

## Git discipline
- Commit after every meaningful unit of work and push immediately.
- Conventional prefixes: feat: / fix: / docs: / chore: / research:.
- Never leave work unpushed; surface push failures immediately.
- Before starting work on a machine with local commits, `git pull --rebase` to absorb commits pushed by other agents.

## Pre-build research pass
- Before any major build phase, run the pre-build research pass skill (`.codex/skills/pre-build-research-pass/SKILL.md` in ctrl-ahead-os).
- Six lanes: official docs → peer-reviewed (EBSCOhost/Scholar/arXiv) → industry benchmarks → community/creator data → open datasets/leaks → contradiction check.
- Time-boxed, source-cited, ends with go/no-go + a plan delta list. Findings saved to `research/` and committed with `research:`.

## Evidence standards
- Numbers over adjectives; source every claim or label it UNVERIFIED.
- Confidence tiers: first-party > peer-reviewed > industry > community > anecdote.
- When a metric is owner-only (e.g., YouTube's viewed-vs-swiped-away), say so and design a first-party measurement loop instead of guessing.