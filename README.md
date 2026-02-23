# quasar-typing

A small Python project for pydantic-compatible typing utilities.

## Features

- Array type definitions and utilities
- DataFrame support
- Path handling
- Type bounds and compound models
- Miscellaneous utilities

## Installation

### Development Installation

```bash
pip install -e ".[dev]"
```

### With Documentation Tools

```bash
pip install -e ".[docs]"
```

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
black src/quasar_typing tests/
isort src/quasar_typing tests/
flake8 src/quasar_typing tests/
mypy src/quasar_typing
```

## Project Structure

```
quasar-typing/
├── src/quasar_typing/          # Main package
│   ├── arrays/                 # Array utilities
│   ├── dataframe/              # DataFrame support
│   ├── paths/                  # Path handling
│   ├── misc/                   # Miscellaneous utilities
│   ├── bounds.py              # Type bounds
│   └── compound_model.py       # Compound model definitions
├── tests/                      # Unit tests
├── docs/                       # Documentation
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## License

MIT License - see LICENSE file for details