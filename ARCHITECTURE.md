# Architecture

See README.md for terminology and the canonical 10-step workflow. This
document covers how the project is built on top of `mini-swe-agent`
(https://github.com/SWE-agent/mini-swe-agent), which is the core engine,
not an incidental dependency.

## mini-swe-agent primitives in play

- `Agent` (`DefaultAgent` + `AgentConfig`, pydantic, subclassable): the
  decision loop. Config carries `system_template` / `instance_template`
  (Jinja2), step/cost/wall-time limits, and an `output_path` for
  trajectory persistence.
- `Model`: a litellm wrapper. Each `Model` instance is bound to one
  litellm model string, so `swe-llm` and `work-llm` are just two
  independently configured `Model` instances — no custom multi-provider
  plumbing needed. Model choice per role comes from
  `PLAN_LOOP_SWE_LLM_MODEL` / `PLAN_LOOP_WORK_LLM_MODEL` (see
  `.env.example`).
- `Environment`: executes bash actions (local, Docker, Podman, ...).
  Only relevant when a role actually needs to touch a filesystem/repo.

## Milestone 1: bare-minimum loop

Resolved in
[`docs/decisions/0001-milestone-1-work-llm-as-bash.md`](docs/decisions/0001-milestone-1-work-llm-as-bash.md):
`work_llm` is not an agent at all — it's the bash command `codex exec`,
run by `swe_agent` like any other shell action. `swe_agent` is a stock
mini-swe-agent `DefaultAgent` (real `Model` + real local `Environment`);
the only project-specific piece is its `system_template`, which forbids
it from doing the work itself and requires delegating via `codex exec`.
Each user task is one independent `swe_agent.run(task)` call — no
cross-task memory yet.

This covers a simplified variant of the README's workflow (no
plan/amend/accept cycle — see issue #2). The full 10-step workflow,
cross-task memory, and structured training-data capture beyond
mini-swe-agent's own trajectory files remain open for a later milestone.

## Repo layout

```
src/plan_loop/
├── configs/
│   └── swe_agent.yaml   # swe_agent's AgentConfig: system/instance templates, limits
├── agents/
│   └── swe_agent.py     # build_swe_agent(): wires Model + local Environment + DefaultAgent
├── prompts/             # plan_task_prompt / plan_amend_prompt — future milestones
├── models.py            # Task, ActionPlan, Feedback — mirrors README's terminology table
├── config.py            # env var loading (PLAN_LOOP_SWE_LLM_MODEL / PLAN_LOOP_WORK_LLM_MODEL)
├── loop.py              # the milestone-1 REPL loop
└── cli.py               # entry point
```
