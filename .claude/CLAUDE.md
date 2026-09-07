# plan-loop project instructions

This file supplies the project-specific rules referenced by the global
agent instructions (git workflow, knowledge persistence, layout,
document layout, common workflow). It overrides default behavior for
work in this repo.

## Before starting any work

Always check whether the workspace is stale before doing anything else:

- `git fetch origin` and compare the current branch against
  `origin/master` (and its own remote tracking branch, if any).
- If behind, sync (fast-forward merge/rebase when there's no divergence)
  before making new changes, and say so.
- If diverged in a way that isn't a clean fast-forward, stop and ask
  before merging/rebasing.

## GitHub as the official record

When fixing an issue or addressing review comments on a PR, post the
substantive answer as a comment on that GitHub issue/PR (`gh issue
comment`, `gh pr comment`, or a reply to the specific review thread via
`gh api`) — that comment is the official answer. In chat, only give a
short summary and a link to the comment; don't duplicate the full
answer in chat.

## Git workflow

- One topic branch per change, PR into `master` for review — don't push
  directly to `master`.
- Prefer small, reviewable commits with messages that explain *why*.

## Development workflow

This project uses `uv` + `just`. Common commands:

- `just install` — sync dependencies (incl. dev group)
- `just lint` / `just fmt` — ruff check / format
- `just test` — run pytest
- `just run` — run the `plan-loop` CLI

A `flake.nix` devshell pins Python/uv/just for anyone using Nix;
it's optional, not required, to work in this repo.

## Layout

- `README.md` — vision and canonical terminology; keep `models.py` in
  sync with the Terminologies table.
- `ARCHITECTURE.md` — how the project maps onto `mini-swe-agent`
  (the core engine); open design questions live here until resolved.
- `docs/decisions/` — one file per non-obvious design decision (ADR
  style: context, decision, consequences).
- `src/plan_loop/` — package source; see ARCHITECTURE.md for the
  breakdown of `configs/`, `prompts/`, `agents/`.
- `tests/` — pytest suite.
