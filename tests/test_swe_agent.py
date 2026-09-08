from minisweagent.agents.default import DefaultAgent

from plan_loop.agents.swe_agent import build_swe_agent


def test_build_swe_agent_wires_a_default_agent():
    agent = build_swe_agent("test-model")
    assert isinstance(agent, DefaultAgent)


def test_cost_tracking_ignores_unregistered_model_errors():
    # Otherwise unregistered/local models (e.g. ollama_chat/...) hard-fail
    # every call, since litellm has no pricing data for them.
    agent = build_swe_agent("test-model")
    assert agent.model.config.cost_tracking == "ignore_errors"


def test_system_template_forces_codex_exec_delegation():
    agent = build_swe_agent("test-model")
    agent.extra_template_vars |= {"task": "do the thing", "work_llm_model": "gpt-5-codex"}
    rendered = agent._render_template(agent.config.system_template)
    assert "codex exec -m gpt-5-codex" in rendered
    assert "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT" in rendered


def test_system_template_forbids_repo_exploration():
    agent = build_swe_agent("test-model")
    agent.extra_template_vars |= {"task": "do the thing", "work_llm_model": "gpt-5-codex"}
    rendered = agent._render_template(agent.config.system_template)
    assert "read-only inspection" not in rendered
    assert "EXACTLY THREE allowed bash commands" in rendered


def test_instance_template_renders_the_task():
    agent = build_swe_agent("test-model")
    agent.extra_template_vars |= {"task": "do the thing", "work_llm_model": "gpt-5-codex"}
    rendered = agent._render_template(agent.config.instance_template)
    assert "do the thing" in rendered
