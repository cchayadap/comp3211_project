# Test Coverage Report (Deliverable 4b)

Line coverage of the `model` package by the unit tests in `tests/`.

- Date: 2026-10-18
- Python: 3.14.6
- Tool: Coverage.py 7.16.2 (dev-only, not used by the system)
- Result: 31 tests run, all pass (30 model tests, 1 controller test)

| File | Statements | Missed | Coverage |
|---|---|---|---|
| model/\_\_init\_\_.py | 5 | 0 | 100% |
| model/collection.py | 31 | 0 | 100% |
| model/criteria.py | 133 | 0 | 100% |
| model/records.py | 88 | 0 | 100% |
| model/storage.py | 35 | 0 | 100% |
| **Total** | **292** | **0** | **100%** |

Re-run and update this table whenever `model/` or the tests change.

## How to reproduce
Run from the project root:

    py -3 -m pip install coverage
    py -3 -m coverage run --source=model -m unittest discover -s tests -t .
    py -3 -m coverage report -m
