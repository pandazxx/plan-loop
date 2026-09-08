from types import SimpleNamespace

from plan_loop.loop import run_task


class StubAgent:
    def __init__(self, result):
        self._result = result
        self.calls = []
        self.config = SimpleNamespace(output_path=None)

    def run(self, task, **kwargs):
        self.calls.append((task, kwargs))
        return self._result


def test_run_task_returns_submission():
    agent = StubAgent({"exit_status": "Submitted", "submission": "digest text"})
    assert run_task(agent, "gpt-5-codex", "do the thing", "runs/0001.json") == "digest text"
    assert agent.calls == [("do the thing", {"work_llm_model": "gpt-5-codex"})]
    assert agent.config.output_path == "runs/0001.json"


def test_run_task_falls_back_when_no_submission():
    agent = StubAgent({"exit_status": "LimitsExceeded", "submission": ""})
    assert "LimitsExceeded" in run_task(agent, "gpt-5-codex", "do the thing", "runs/0001.json")
