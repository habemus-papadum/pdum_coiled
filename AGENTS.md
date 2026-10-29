# AGENTS.md

This file provides guidance to AI agents when working with code in this repository.

## Project Overview

This is a Python library called `coiled` (package name: `coiled`, module name: `pdum.coiled`). Coiled utils

The project uses a modern Python toolchain with UV for dependency management.

## Important Rules

### Versions and releases
`ship` (habemus-papadum-ship) releases this repository's one package,
`habemus-papadum-coiled`. It has its own version and tag series
(`habemus-papadum-coiled-v<version>`); between releases the manifest says
`<last release>+dev`. Never edit a version field by hand. `__version__` reads
the installed metadata.

To release, ask the operator. When they agree, run the release workflow:
`gh workflow run release.yml -f bump=minor -f dry_run=false` (run with
`dry_run=true` first to see the plan). Do not publish from this machine.

The widgets workspace (`widgets/`, `@habemus-papadum/coiled-widgets`) is
`private: true`: it is not published to npm and ship does not version it. Its
built bundle ships inside the wheel.

Do not update repositories that consume this package; their scheduled refresh
does that. The one exception: if your change needs a newer release of another
of our packages, raise that package's floor here. Do not pin a
`habemus-papadum-*` or `@habemus-papadum/*` package to an exact version without
a reason on the same line or in `[tool.ship.pins]`. Never commit a `path` or
`editable` entry in `[tool.uv.sources]`, or a `link:`/`file:` dependency
(`pnpm link` writes one). Run `uv run ship deps check` before you finish.

## Development Commands

### Environment Setup
```bash
# Bootstrap the full toolchain (uv sync, pnpm install, widget build, hooks)
./scripts/setup.sh
```

**Important for Development**:
- Plain `uv sync` and `uv run` keep the locked versions; the lockfile changes only when a command is asked to change it (`uv add`, `uv remove`, `ship deps refresh`). CI uses `--locked`.
- Re-run `./scripts/setup.sh` whenever dependencies change

### Testing
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

### Releasing
```bash
# Plan a release (operators run the real one through the release workflow)
uv run ship release habemus-papadum-coiled --bump minor --dry-run

# Check the release policy: development links, lockfiles, pins, version marker
uv run ship deps check
```

### TypeScript widgets (pnpm)
```bash
# Workspace-wide lint
pnpm lint

# Focus on the widgets package
pnpm --filter '@habemus-papadum/coiled-widgets' typecheck
pnpm --filter '@habemus-papadum/coiled-widgets' build:python
pnpm --filter '@habemus-papadum/coiled-widgets' test:coverage
```

- Widget bundle lives in `widgets/`; the compiled JS is copied into `src/pdum/coiled/widgets/index.js`
- Never commit `widgets/dist/`—it is generated
- After changing widget source, run `build:python` and commit the regenerated `src/pdum/coiled/widgets/index.js`

## Architecture

### Project Structure
- **src/pdum/coiled/**: Main package source code (src-layout)
  - `__init__.py`: Package initialization and version
- **tests/**: Test suite using pytest
  - `test_example.py`: Example tests

### Key Constraints
- **Python Version**: Requires Python 3.14+
- **Dependency Management**: Uses UV for Python and pnpm for the widgets workspace; uv.lock is committed
- **Build System**: Hatchling builds distributions; `ship` runs the build at release time

### Code Standards
- **Ruff Configuration**:
  - Target: Python 3.14
  - Line length: 120 characters
  - Linting rules: E (pycodestyle errors), F (pyflakes), W (warnings), I (isort)
- **Type Hints**: Use type hints where appropriate
- **Docstrings**: NumPy style, include Parameters, Returns, Raises sections

### Testing Strategy
- Test files must start with `test_` prefix
- Test classes must start with `Test` prefix
- Test functions must start with `test_` prefix
- Tests run with `-s` flag (no capture) by default
- Coverage reporting: use `--cov=src/pdum/coiled --cov-report=xml --cov-report=term`

### Testing Configuration
The pytest configuration is in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-s"
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

Coverage configuration is also in `pyproject.toml`:
```toml
[tool.coverage.run]
source = ["src/pdum/coiled"]
relative_files = true
omit = [
    "*/tests/*",
    "*/testing.py",
]
```

## CI/CD

### Continuous Integration
The project uses GitHub Actions for CI (`.github/workflows/ci.yml`):
- Runs on every push to main and pull requests
- Executes pnpm lint/build/test for the widgets workspace (and publishes a TypeScript coverage badge on main)
- Executes linting with ruff
- Runs unit tests with coverage reporting
- Posts coverage report as a PR comment

### Documentation Deployment
Documentation is deployed to GitHub Pages (`.github/workflows/docs.yml`) on
every push to `main`, or by hand via workflow_dispatch.

### Release Process
Releases run from the `release` workflow (`.github/workflows/release.yml`),
which calls the reusable workflow in `habemus-papadum/pdum_ship`. It waits for
`ci.yml` to pass on the same commit, then runs `ship release habemus-papadum-coiled`:
1. Reads the last tag `habemus-papadum-coiled-v<version>` and applies the requested bump
2. Writes the release version into `pyproject.toml` and re-locks
3. Builds, runs the tests, publishes to PyPI with the `PYPI_API_TOKEN` secret
4. Commits, tags `habemus-papadum-coiled-v<version>`, pushes commit and tag together
5. Creates the GitHub release
6. Writes `<version>+dev` back and pushes

Versions follow `X.Y.Z+dev` → `X.Y.Z` (tagged) → `X.Y.Z+dev`.
