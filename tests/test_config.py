import pytest

from plan_loop.config import ConfigError, load_config


def test_load_config_requires_both_models(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # no .env here to interfere
    monkeypatch.delenv("PLAN_LOOP_SWE_LLM_MODEL", raising=False)
    monkeypatch.delenv("PLAN_LOOP_WORK_LLM_MODEL", raising=False)
    with pytest.raises(ConfigError):
        load_config()


def test_load_config_returns_both_models(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PLAN_LOOP_SWE_LLM_MODEL", "anthropic/claude-opus-4-8")
    monkeypatch.setenv("PLAN_LOOP_WORK_LLM_MODEL", "gpt-5-codex")
    assert load_config() == ("anthropic/claude-opus-4-8", "gpt-5-codex")
