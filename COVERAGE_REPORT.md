# Test Coverage Report (Deliverable 4b)

Line coverage of the `model` package by the unit tests in `tests/`.

- Date: 2026-10-10
- Python: 3.14.6
- Tool: Coverage.py 7.16.2 (dev-only, not used by the system)
- Result: 16 tests run, all pass

| File | Statements | Missed | Coverage | Missed lines |
|---|---|---|---|---|
| model/\_\_init\_\_.py | 5 | 0 | 100% | - |
| model/collection.py | 31 | 2 | 94% | 16, 40 |
| model/criteria.py | 127 | 12 | 91% | 42, 88-89, 102-103, 107-108, 156, 161-163, 179 |
| model/records.py | 76 | 3 | 96% | 37, 85, 115 |
| model/storage.py | 27 | 1 | 96% | 27 |
| **Total** | **266** | **18** | **93%** | |

## How to reproduce
Run from the project root:

    py -3 -m pip install coverage
    py -3 -m coverage run --source=model -m unittest discover -s tests -t .
    py -3 -m coverage report -m
