# Repository-local AGENTS.md for tecsoo-letolto
Applies only to this repository.

The parent rules in `e:\codex_works\AGENTS.md` apply first (shared safety, PowerShell rules, encoding safety, and cross-repo boundaries).

---

## State file

- This repository uses `STATE.md` as the authoritative project memory.
- Read `STATE.md` before continuing previous work.
- Update `STATE.md` after meaningful changes, bug fixes, failed attempts, test results, or release steps.

---

## Local workflow basics

- Start with `git status` before making changes.
- Prefer small, reviewable diffs; avoid unrelated refactors.
- Keep files UTF-8; avoid accidental line-ending churn.
- In PowerShell, avoid `&&` command chaining.
