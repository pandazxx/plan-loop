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

# Run the plan-loop CLI (placeholder until loop.py is implemented)
run *args:
    uv run plan-loop {{args}}
