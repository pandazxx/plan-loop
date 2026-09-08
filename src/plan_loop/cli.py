"""Entry point for the plan-loop CLI."""

import sys

from plan_loop.config import ConfigError, load_config
from plan_loop.loop import run_repl


def main() -> None:
    try:
        swe_llm_model, work_llm_model = load_config()
    except ConfigError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1) from e
    run_repl(swe_llm_model, work_llm_model)


if __name__ == "__main__":
    main()
