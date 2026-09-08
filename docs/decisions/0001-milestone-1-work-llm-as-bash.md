# 0001: work_llm is a bash command, not an agent

## Context

Milestone 1 (github.com/pandazxx/plan-loop/issues/2) asks for a bare-minimum
version of the workflow, with `codex` as `work_llm`:

```
User --task prompt--> swe --task prompt--> swe_agent --work prompt--> work_llm --work result--> swe_agent --digest--> User --next loop-->...
```

An earlier draft of this design assumed `work_llm` would be its own
mini-swe-agent `DefaultAgent` (real `Model` + real local `Environment`),
run and orchestrated from within `swe_agent`. That assumption was wrong.

## Decision

- `work_llm` is not an agent, a `Model`, or an `Environment` of its own.
  It is one bash command that `swe_agent` runs like any other:
  `codex exec -m <model> --sandbox workspace-write -o <file> "<prompt>"`.
- `swe_agent` is a stock mini-swe-agent `DefaultAgent`: a real litellm
  `Model` (`PLAN_LOOP_SWE_LLM_MODEL`) and a real local `Environment`. No
  custom `Agent`/`Environment` subclass is needed. The only
  project-specific piece is `swe_agent`'s `system_template`
  (`src/plan_loop/configs/swe_agent.yaml`), which forbids it from doing
  the work itself and requires it to delegate via `codex exec`.
- "work prompt" and "work result" are therefore not special types -
  they're just the command `swe_agent` chooses to run and the observation
  mini-swe-agent's `LocalEnvironment` returns for it.
- `PLAN_LOOP_WORK_LLM_MODEL` is the model id passed to `codex exec -m`,
  not a litellm string - codex handles its own provider auth.
- Each task is one independent `swe_agent.run(task)` call. mini-swe-agent's
  `run()` resets message history at the start, so there is no memory
  across tasks in milestone 1. `swe_agent` still finishes each task via
  the standard mini-swe-agent submission convention (`COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`),
  which is used as the digest shown to the user.

## Consequences

- No custom `Environment`/`Agent` code for milestone 1: a system prompt,
  a YAML config, and a small CLI loop are enough.
- The `codex` CLI is an external prerequisite (not managed by uv or the
  nix flake) - it must be installed and authenticated separately; `just
  doctor` checks it's on `PATH`.
- Cross-task memory, the plan/amend/accept cycle (README's full 10-step
  workflow), and structured training-data capture are explicitly out of
  scope for milestone 1 and remain open for a later milestone.
