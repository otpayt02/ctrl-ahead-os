# AGENTS.md — Operating rules for every agent (Codex, Claude Code, Perplexity, etc.) working in ctrl-ahead-os

## Core rules

1. **Numbered task blocks.** Every request with 2+ tasks gets restated as a numbered task block first. Execute, then report results back under the SAME numbers. Each report item carries a status (DONE / PARTIAL / BLOCKED / HELD) and quantitative evidence (counts, paths, commit hashes, percentages). See `.codex/skills/numbered-task-reporting/SKILL.md`.
2. **Commit and push after every meaningful unit of work.** Conventional commit prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `research:`. Never leave work unpushed. If a push fails, surface the error immediately — never silently continue.
3. **Pre-build research pass.** Before starting any major build phase, run the last-ditch sanity-check research sweep defined in `.codex/skills/pre-build-research-pass/SKILL.md`. Findings get saved to a `research/` folder and committed with the `research:` prefix.
4. **Numbers over vibes.** Every claim gets a source or is labeled UNVERIFIED. Distinguish first-party data, peer-reviewed research, industry benchmarks, community data, and anecdote.
5. **Data invariants.** `script_inputs.json`, `script_inputs.md`, `*.db`, scraped exports, and API keys stay git-ignored. Never commit scraped databases.
6. **UI work follows UI_RULES.md** (cinematic, UX-first). **Sequencing follows ROADMAP.md**; update ROADMAP.md when a phase completes.
7. **Before pushing from a machine with local-only commits, `git pull --rebase` first** to absorb commits pushed from other agents (e.g., API-pushed commits from Perplexity).

## Skill index

- `.codex/skills/numbered-task-reporting/SKILL.md` — numbered task block response format
- `.codex/skills/pre-build-research-pass/SKILL.md` — final pre-build research/sanity-check sweep

## Global Codex instructions

The copy-paste version for Codex Settings → Global Instructions lives in `CODEX_GLOBAL_INSTRUCTIONS.md`.