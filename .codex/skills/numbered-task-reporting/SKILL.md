---
name: numbered-task-reporting
description: Format every multi-task response as numbered task blocks — restate each requested task as a numbered item, execute in order, and report results back under the same numbers with status and quantitative evidence. Use when the user asks for task blocks, numbered reporting, or "answer everything in this prompt / do all requested tasks".
---

# Numbered Task Reporting

## When to use
Any request containing two or more distinct tasks, or any request saying "answer everything", "do all requested tasks", or asking for a task block.

## Procedure
1. **Parse** the request into discrete tasks.
2. **Restate** each task as a numbered item with a short imperative label.
3. **Execute** in order; batch independent operations.
4. **Report** back under the same numbers.

## Report format per task
`N. TASK LABEL — STATUS. [numbers: X files created, Y sources found, commit abc1234, Z% target]`

Statuses: DONE / PARTIAL (what's missing) / BLOCKED (reason) / HELD (awaiting: X).

## Rules
- Never silently drop a task — every numbered item appears in the report.
- Never renumber between restatement and report.
- Numbers over adjectives: "3 commits pushed", not "several commits pushed".
- New work discovered mid-execution attaches to the relevant task number as a sub-note, not a new block.
- Irreversible external actions (push, send, publish) still require explicit user confirmation before executing.