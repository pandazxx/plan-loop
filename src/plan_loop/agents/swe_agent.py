"""Builds the swe_agent: a stock mini-swe-agent DefaultAgent whose system
prompt makes `codex exec` its only way to get work done (see
docs/decisions/0001-milestone-1-work-llm-as-bash.md).
"""

from pathlib import Path

import yaml
from minisweagent.agents import get_agent
from minisweagent.agents.default import DefaultAgent
from minisweagent.environments import get_environment
from minisweagent.models import get_model

CONFIG_PATH = Path(__file__).parent.parent / "configs" / "swe_agent.yaml"


def build_swe_agent(swe_llm_model: str) -> DefaultAgent:
    config = yaml.safe_load(CONFIG_PATH.read_text())
    model = get_model(config=config.get("model", {}) | {"model_name": swe_llm_model})
    env = get_environment(config.get("environment", {}), default_type="local")
    return get_agent(model, env, config.get("agent", {}), default_type="default")
