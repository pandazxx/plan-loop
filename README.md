# Plan-loop

## Objective

- Use mini-swe-agent as orchestrator (named `swe` for short). It runs a LLM agent (named `swe-agent`) to instruct another LLM agent (named `target-agent`) to plan and execute.
- The prompt that `swe` feed to `swe-agent`, the `swe-agent` feed to `target-agent` and the planning result will be further training material. The prompt that `swe` feed to `swe-agent` is the optimization target.
