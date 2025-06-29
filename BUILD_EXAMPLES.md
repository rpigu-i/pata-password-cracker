# Building with Different Backends

This project now supports multiple build backends. Here are examples of how to use them:

## Using setuptools backend (current default)
```bash
# Standard build
python -m build

# Development install
pip install -e .

# Install with development dependencies  
pip install -e ".[dev]"
```

## Using Poetry backend

To use Poetry instead of setuptools, replace the `[build-system]` section in `pyproject.toml`:

```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Then you can use Poetry commands:
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Install with dev dependencies
poetry install --with dev

# Build package
poetry build

# Run commands
poetry run python -m pata_password_cracker --help

# Add dependencies
poetry add new-package

# Update dependencies
poetry update
```

## Installing NLTK Dependencies

After installation with either method, run:
```bash
python install_nltk_deps.py
```

Or manually:
```bash
python -m nltk.downloader wordnet
```

Both approaches preserve all the original functionality while providing modern Python packaging support.