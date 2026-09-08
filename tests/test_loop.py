from plan_loop.loop import run_task


class StubAgent:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def run(self, task, **kwargs):
        self.calls.append((task, kwargs))
        return self._result


def test_run_task_returns_submission():
    agent = StubAgent({"exit_status": "Submitted", "submission": "digest text"})
    assert run_task(agent, "gpt-5-codex", "do the thing") == "digest text"
    assert agent.calls == [("do the thing", {"work_llm_model": "gpt-5-codex"})]


def test_run_task_falls_back_when_no_submission():
    agent = StubAgent({"exit_status": "LimitsExceeded", "submission": ""})
    assert "LimitsExceeded" in run_task(agent, "gpt-5-codex", "do the thing")
