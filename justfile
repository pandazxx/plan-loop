set dotenv-load := true

# Install dependencies (incl. dev group)
install:
    uv sync --group dev

# Lint
lint:
    uv run ruff check .

# Format
fmt:
    uv run ruff format .

# Run tests
test:
    uv run pytest

# Run the plan-loop CLI
run *args:
    uv run plan-loop {{args}}

# Check for external prerequisites not managed by uv/nix
doctor:
    command -v codex >/dev/null || (echo "codex CLI not found: https://github.com/openai/codex" && exit 1)
    echo "codex CLI found: $(command -v codex)"
