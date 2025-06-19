# Contributing to TabbySet

To contribute to TabbySet, you must have `uv` installed. Please refer to the [uv documentation](https://docs.astral.
sh/uv/getting-started/installation/).

After installing `uv`, you can clone the repository and set up the development environment:

```bash
git clone https://github.com/exactpro/tabbyset
cd tabbyset
uv sync
```

## Running tests

Tests support built-in UnitTest framework:

```bash
python -m unittest discover tests
```

Running tests with coverage:

```bash
uv run -m coverage run -m unittest discover tests
```

Display coverage report:

```bash
uv run -m coverage report
```

## How to release a new version

Release pipeline runs every push to the `main` branch. It checks if version in `pyproject.toml` is greater than the 
last release version. If it is, it will build a new release and upload it to PyPI and reflect it in a GitHub Release.

Version should be updated using `uv version` command. We strongly encourage using `--bump` option, which follows 
[semantic versioning rules](https://semver.org/).

There are commands to make a patch / minor / major release:

```bash
uv version --bump patch
uv version --bump minor
uv version --bump major
```