"""Entry point for the plan-loop CLI."""

import logging
import sys

from plan_loop.config import ConfigError, is_debug, load_config
from plan_loop.loop import run_repl


def _setup_debug_logging() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(name)s: %(levelname)s: %(message)s")
    import litellm

    litellm.set_verbose = True


def main() -> None:
    try:
        swe_llm_model, work_llm_model = load_config()
    except ConfigError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1) from e
    if is_debug():
        _setup_debug_logging()
    run_repl(swe_llm_model, work_llm_model)


if __name__ == "__main__":
    main()
