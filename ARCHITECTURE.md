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

## Open design questions

The mapping between the README's 10-step workflow and mini-swe-agent's
`Agent`/`Model`/`Environment` triad — specifically how the swe-llm
prompt-authoring step (steps 2 and 6) is implemented, and how the
work-llm execution step (step 10) is scoped — is **not yet decided**.
An earlier draft of this document assumed a full `DefaultAgent` for
swe-llm; that assumption was flagged as wrong and the detailed design
is deferred. Record the actual decision in `docs/decisions/` once made.

What is settled:

- Different models per role, configured via env vars (done — see
  `.env.example`).
- mini-swe-agent's own trajectory files (`output_path`,
  `serialize()`/`save()`) are the natural basis for the "training
  material" this project is meant to produce, tagged with role and
  prompt-template version. Whether `storage.py` wraps that directly or
  needs its own format is part of the deferred design.

## Repo layout

```
src/plan_loop/
├── configs/     # mini-swe-agent AgentConfig YAML overrides, per role
├── prompts/     # plan_task_prompt / plan_amend_prompt templates (versioned)
├── agents/      # plan-loop-specific Agent subclasses/wrappers
├── models.py    # Task, ActionPlan, Feedback — mirrors README's terminology table
├── loop.py      # the 10-step state machine (placeholder)
└── cli.py       # entry point (placeholder)
```
