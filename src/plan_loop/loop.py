"""Milestone 1 bare-minimum loop (see README.md's Typical workflow, simplified):

    User --task--> swe_agent --codex exec--> work_llm --result--> swe_agent --digest--> User

No plan/amend/accept cycle yet - each task is a single, independent
swe_agent.run() call. See docs/decisions/0001-milestone-1-work-llm-as-bash.md.
"""

from pathlib import Path

from minisweagent.agents.default import DefaultAgent

from plan_loop.agents.swe_agent import build_swe_agent

PROMPT = "task> "
EXIT_COMMANDS = {"exit", "quit"}
RUNS_DIR = Path("runs")


def run_task(agent: DefaultAgent, work_llm_model: str, task: str, output_path: Path) -> str:
    agent.config.output_path = output_path
    result = agent.run(task, work_llm_model=work_llm_model)
    return result.get("submission") or f"(no submission; exit_status={result.get('exit_status')})"


def run_repl(swe_llm_model: str, work_llm_model: str) -> None:
    agent = build_swe_agent(swe_llm_model)
    task_number = 0
    while True:
        try:
            task = input(PROMPT).strip()
        except EOFError:
            break
        if not task or task in EXIT_COMMANDS:
            break
        task_number += 1
        output_path = RUNS_DIR / f"{task_number:04d}.json"
        try:
            print(run_task(agent, work_llm_model, task, output_path))
        except Exception as e:  # keep the REPL alive across task failures
            print(f"task failed: {e}")
        print(f"(full trajectory: {output_path})")
