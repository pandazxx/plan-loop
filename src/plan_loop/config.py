import os

from dotenv import load_dotenv

SWE_LLM_MODEL_ENV = "PLAN_LOOP_SWE_LLM_MODEL"
WORK_LLM_MODEL_ENV = "PLAN_LOOP_WORK_LLM_MODEL"
DEBUG_ENV = "PLAN_LOOP_DEBUG"


class ConfigError(RuntimeError):
    pass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"{name} is not set. Copy .env.example to .env and fill it in.")
    return value


def load_config() -> tuple[str, str]:
    """Load env vars, returning (swe_llm_model, work_llm_model)."""
    load_dotenv()
    return _require_env(SWE_LLM_MODEL_ENV), _require_env(WORK_LLM_MODEL_ENV)


def is_debug() -> bool:
    return os.getenv(DEBUG_ENV, "").lower() in {"1", "true", "yes"}
