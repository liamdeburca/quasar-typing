# quasar-typing

A small Python project for pydantic-compatible typing utilities.

## Features

- Array type definitions and utilities
- DataFrame support
- Path handling
- Type bounds and compound models
- Miscellaneous utilities

## Installation

```bash
pip install .
```

## Development

### Running Tests

```bash
pytest
```

## Project Structure

The module contains the following submodules:

1. `astropy`: Astropy-related typing utilities.
    - `coordinates`
    - `cosmology`
    - `fits`
    - `modeling`
    - `table`
    - `units`
2. `errors`: Custom error types.
3. `numpy`: Numpy-related typing utilities: validating shapes, data types, and other properties of arrays, among other things.
    - `random`: Typing utilities for `numpy.random`
4. `pathlib`: `pathlib.Path`-related typing utilities: validating existant/new paths, path extensions, etc.
5. `scipy`: Scipy-related typing utilities.
    - `optimize`
    - `sparse`
    - `stats`
6. `bounds`
7. `cachetools`
8. `dynesty`: requires the `dynesty` package.
9. `emcee`: requires the `emcee` package.
10. `h5py`: requires the `h5py` package.
11. `literals`: Typing utilities for literal types.
12. `logging`
13. `multiprocessing`
14. `pandas`: requires the `pandas` package.
15. `re`: Typing utilities for validating regex pattern strings.
16. `string_selections`: Validating sets of strings.
17. `misc`: Miscellaneous typing utilities.
18. `utils`: Utilities for common validation tasks.

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