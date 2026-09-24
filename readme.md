# ci-demo-week6

CI demo project for Week 6. Implements late-fee calculation for the QuackLoan rubber-duck lending library, with unit tests run in GitHub Actions.

## Features

- `DuckFine` class for per-member fine tracking.
- 2-day grace period, $0.50/day rate, 2x deluxe multiplier, $5.00 cap.
- Accumulating `total_owed` balance per member.
- Validation for negative input.
- `unittest` suite with 11 tests.
- GitHub Actions CI on `push` to `main` and `pull_request`.

## Project Structure

```
ci-demo-week6/
  .github/workflows/tests.yml  # CI workflow
  duck_test/
    duckfine.py                # DuckFine implementation
    test_duckfine.py           # unittest suite
  testpush.md                  # scratch file
  readme.md
```

## Requirements

- Python 3.13 (per CI; any Python 3.x should work)
- No third-party dependencies. Standard library only.

## Installation

```bash
git clone <repo-url>
cd ci-demo-week6
python --version
```

No install step required.

## Usage

```python
from duck_test.duckfine import DuckFine
# or, from inside duck_test/:
# from duckfine import DuckFine

d = DuckFine('m1')
print(d.charge(0))   # 0.0 - on time
print(d.charge(3))   # 0.5 - 1 chargeable day
print(d.charge(6, deluxe=True))  # 4.0
print(d.total_owed)  # accumulated total
```

If running from `duck_test/` directory:

```bash
cd duck_test
python -c "from duckfine import DuckFine; d=DuckFine('m1'); print(d.charge(6))"
```

## API Reference

### `DuckFine(member_id)`

Creates a tracker for one member.

- `member_id: str` - stored as `member_id`.
- `total_owed: float` - initialized to `0.0`, accumulates across `charge()` calls.

Class constants:

| Constant | Value | Meaning |
|---|---|---|
| `DAILY_FEE` | `0.50` | Dollars per chargeable day |
| `GRACE_DAYS` | `2` | First N days late forgiven |
| `MAX_FEE` | `5.00` | Per-charge cap |

### `charge(days_late, deluxe=False) -> float`

Calculates one fine, adds it to `total_owed`, returns it.

- `days_late: int` - days past due. Must be `>= 0`, else raises `ValueError`.
- `deluxe: bool` - if `True`, fee is doubled before capping. Default `False`.

Formula:

```
chargeable = max(0, days_late - GRACE_DAYS)
fee = chargeable * DAILY_FEE
if deluxe: fee *= 2
fee = min(fee, MAX_FEE)
total_owed += fee
```

Examples:

| `days_late` | `deluxe` | Return | Notes |
|---|---|---|---|
| 0 | False | 0.0 | on time |
| 2 | False | 0.0 | within grace |
| 2 | True | 0.0 | grace applies even if deluxe |
| 3 | False | 0.50 | 1 x 0.50 |
| 4 | False | 1.00 | 2 x 0.50 |
| 6 | False | 2.00 | 4 x 0.50 |
| 6 | True | 4.00 | 4 x 0.50 x 2 |
| 12 | True | 5.00 | (10 x 0.50 x 2)=10.00 capped |
| 100 | False | 5.00 | capped |

Error case:

```python
d.charge(-1)  # raises ValueError("days_late must not be negative")
```

`total_owed` accumulation:

```python
d = DuckFine('m1')
d.charge(3)  # 0.50
d.charge(4)  # 1.00
d.total_owed # 1.50
```

## Testing

Run from repo root:

```bash
python -m unittest discover -s duck_test -v
```

Expected: 11 tests, all pass.

Test coverage in `test_duckfine.py`:

- init sets member and zero owed
- no fee when on time / within grace
- fee after grace, scaling per day
- deluxe doubling, deluxe within grace still zero
- cap at max for standard and deluxe
- total accumulation
- negative days raises `ValueError`

## Continuous Integration

Workflow: `.github/workflows/tests.yml`

- Name: `Tests`
- Triggers: `push` to `main`, all `pull_request`
- Runner: `ubuntu-latest`
- Steps:
  1. `actions/checkout@v4`
  2. `actions/setup-python@v5` with `python-version: "3.13"`
  3. `python -m unittest discover -s duck_test -v`

No lint, build, or deploy jobs.

## Notes / Limitations

- `total_owed` is in-memory only; no persistence.
- Monetary values use `float`; no decimal rounding applied beyond cap logic. Tests use `assertAlmostEqual` where needed.
- `days_late` is assumed integer; floats are not explicitly handled.
- `MAX_FEE` applies per `charge()` call, not to `total_owed`.
