# coiled

[![CI](https://github.com/habemus-papadum/pdum_coiled/actions/workflows/ci.yml/badge.svg)](https://github.com/habemus-papadum/pdum_coiled/actions/workflows/ci.yml)
[![TypeScript Coverage](https://raw.githubusercontent.com/habemus-papadum/pdum_coiled/typescript-coverage-badge/typescript-coverage.svg)](https://github.com/habemus-papadum/pdum_coiled/tree/main/widgets)
[![PyPI](https://img.shields.io/pypi/v/coiled.svg)](https://pypi.org/project/habemus-papadum-coiled/)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Coiled utils

## Installation

Install using pip:

```bash
pip install habemus-papadum-coiled
```

Or using uv:

```bash
uv pip install habemus-papadum-coiled
```

## Usage

```python
from pdum import coiled

print(coiled.__version__)
```

## Development

This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

### Setup

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
# Install pnpm (required for the widgets workspace)
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Clone the repository
git clone https://github.com/habemus-papadum/pdum_coiled.git
cd coiled

# Provision the entire toolchain (uv sync, pnpm install, widget build, pre-commit hooks)
./scripts/setup.sh
```

**Important for Development**:
- `./scripts/setup.sh` is idempotent—rerun it after pulling dependency changes
- Use `uv sync --frozen` to ensure the lockfile is respected when installing Python deps
- The widgets live in `widgets/` and are managed with pnpm (see "TypeScript widgets" below)

### Running Tests

```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_example.py

# Run a specific test function
uv run pytest tests/test_example.py::test_version

# Run tests with coverage
uv run pytest --cov=src/pdum/coiled --cov-report=xml --cov-report=term
```

### Code Quality

```bash
# Check code with ruff
uv run ruff check .

# Format code with ruff
uv run ruff format .

# Fix auto-fixable issues
uv run ruff check --fix .
```

### TypeScript widgets (pnpm)

```bash
# Lint the widget source
pnpm lint

# Type-check only the widgets package
pnpm --filter '@habemus-papadum/coiled-widgets' typecheck

# Build the browser bundle and copy it into the Python package
pnpm --filter '@habemus-papadum/coiled-widgets' build:python

# Run Vitest (or add --coverage)
pnpm --filter '@habemus-papadum/coiled-widgets' test
```

### Building

```bash
# Build Python + TypeScript artifacts
./scripts/build.sh

# Or build just the Python distribution artifacts
uv build
```

### Publishing

```bash
# Build and publish to PyPI (requires credentials)
./scripts/publish.sh
```

### Automation scripts

- `./scripts/setup.sh` – bootstrap uv, pnpm, widget bundle, and pre-commit hooks
- `./scripts/build.sh` – reproduce the release build locally
- `./scripts/pre-release.sh` – run the full battery of quality checks
- `./scripts/release.sh` – orchestrate the release (creates tags, publishes to PyPI/GitHub)
- `./scripts/test_notebooks.sh` – execute demo notebooks (uses `./scripts/nb.sh` under the hood)
- `./scripts/setup-visual-tests.sh` – install Playwright browsers for visual tests

## License

MIT License - see LICENSE file for details.
