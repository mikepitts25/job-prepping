# 5. The four-hour testing sprint

"Developing unit tests and automated test capabilities" is what the posting
says the job *is*. This sprint is therefore the highest-value four hours on the
site.

We use a deliberately **boring** program: a shopping basket. No radars, no
tracks, no domain to learn. You already know what a basket costs and what a
discount does, which means every minute goes into the testing rather than into
understanding the thing being tested.

By hour four you will have a small program and 46 tests, you will have written
code test-first, and you will have proved to yourself why a high coverage
number can be worthless.

[Lesson 19](testing-ci.html) is the reference. [Lesson 4](python-sprint.html)
is the Python sprint, and this assumes you have done it or already know basic
Python.

## The rules

1. **Type everything.**
2. **Run `pytest` after every block.** It takes half a second.
3. **When I say break it, break it.** Watching a test fail is the only way to
   learn that it works.
4. **Read the failure output.** pytest prints the actual values. That is the
   whole point of it.

## What I am cutting

| Cut | Why |
| --- | --- |
| Integration and end-to-end tests | Unit testing is the skill that transfers. [Lesson 19](testing-ci.html) has the pyramid. |
| Property-based testing (Hypothesis) | Excellent, not day one. |
| Mutation testing | Mentioned in hour four; a tool for later. |
| `unittest` (the standard library one) | pytest is what teams use. You can read `unittest` once you know pytest. |
| Mocking frameworks in depth | We use fakes, which are better anyway, and one `MagicMock` example. |

## Setup: three minutes, before the clock

```bash
mkdir testsprint && cd testsprint
python3 -m venv .venv
source .venv/bin/activate
pip install pytest pytest-cov
pytest --version
```

Start the clock.

---

## Hour 1: what a test is

### 0:00 to 0:15 — assert, and nothing else

A test is a function whose name starts with `test_`, containing an `assert`.

`assert` means "this had better be true." If it is, **nothing happens at all**.
If it is not, it raises `AssertionError`.

```python
>>> assert 1 + 1 == 2        # true: silence
>>> assert 1 + 1 == 3        # false
AssertionError
```

Silence means pass. That is why a passing suite is quiet.

Make `test_first.py`:

```python
def test_arithmetic_still_works():
    assert 1 + 1 == 2


def test_this_one_fails_on_purpose():
    assert 2 + 2 == 5
```

```bash
pytest -q
```

Read the failure carefully. pytest shows you `assert 4 == 5`, the actual values,
not just "failed." **That is why plain `assert` is enough in Python and you
need no special assertion methods.**

Delete the failing test. Delete the file. Now the real work.

### 0:15 to 0:45 — The program

Create `basket.py`:

```python
"""A shopping basket.

Money is held in whole pence as integers, never as floats. 0.1 + 0.2 is not
0.3 in binary floating point, and a rounding error in a price is the kind of
bug a customer notices.
"""

from dataclasses import dataclass


class BasketError(Exception):
    """Base class for anything this module rejects."""


@dataclass(frozen=True)
class Item:
    """One line in the basket."""

    name: str
    unit_price_pence: int
    quantity: int

    def __post_init__(self):
        if not self.name.strip():
            raise BasketError("name must not be blank")
        if self.unit_price_pence < 0:
            raise BasketError(f"price must not be negative: {self.unit_price_pence}")
        if self.quantity < 1:
            raise BasketError(f"quantity must be at least 1: {self.quantity}")


def line_total(item: Item) -> int:
    """What one line costs, in pence."""
    return item.unit_price_pence * item.quantity


def subtotal(items) -> int:
    """What every line costs together, in pence. An empty basket costs nothing."""
    return sum(line_total(item) for item in items)
```

Two design decisions that exist **because of testing**, and both are worth
saying in an interview:

**Integer pence, not floats.** Floats cannot represent a tenth exactly, so
money arithmetic drifts. Using pence makes every assertion exact:
`assert total == 270`, with no tolerance and no `pytest.approx`.

**Validation in `__post_init__`.** An `Item` that violates the rules cannot be
constructed, so nothing downstream has to defend against one. That converts a
scattering of defensive checks into one place with one test each.

### 0:45 to 1:00 — Your first real tests

```python
import pytest

from basket import BasketError, Item, line_total, subtotal


def test_line_total_multiplies_price_by_quantity():
    assert line_total(Item("apple", 50, 3)) == 150


def test_subtotal_adds_the_lines_up():
    assert subtotal([Item("apple", 50, 3), Item("bread", 120, 1)]) == 270


def test_an_empty_basket_costs_nothing():
    assert subtotal([]) == 0


def test_a_single_line_basket():
    assert subtotal([Item("apple", 50, 1)]) == 50
```

```bash
pytest -q
```

**The names are the specification.** Read them on their own: a line total
multiplies price by quantity, a subtotal adds the lines up, an empty basket
costs nothing. Someone who has never seen the code now knows what it does.
`test_1`, `test_2`, `test_3` would have told them nothing.

**Arrange, Act, Assert** is the shape of every test:

```python
def test_subtotal_adds_the_lines_up():
    items = [Item("apple", 50, 3), Item("bread", 120, 1)]   # Arrange
    result = subtotal(items)                                 # Act
    assert result == 270                                     # Assert
```

One-liners like the versions above are fine when all three fit on a line.

**Do now, five minutes.** Break `line_total` by changing `*` to `+`. Run
pytest. Notice that **three tests fail, not one**, and that the failure output
tells you the expected and actual numbers. Put it back.

**Five minutes off.**

---

## Hour 2: the cases that catch real bugs

### 1:00 to 1:20 — Testing that something is rejected

```python
def test_a_valid_item_is_accepted():
    item = Item("apple", 50, 3)
    assert item.name == "apple"
    assert item.quantity == 3


def test_a_negative_price_is_rejected():
    with pytest.raises(BasketError):
        Item("apple", -1, 1)


def test_the_error_says_what_was_wrong():
    with pytest.raises(BasketError, match="quantity"):
        Item("apple", 50, 0)
```

**`with pytest.raises(...)` passes only if the block raises that exception.** If
the code wrongly accepts the bad value, the test fails. That is how you test a
guard.

**`match=` checks the message**, so you are testing that the *right* error was
raised and not merely that something went wrong. Without it, a test can pass
because of an unrelated crash.

### 1:20 to 1:40 — One test, many cases

When the same logic needs several inputs, do not write five near-identical
functions:

```python
@pytest.mark.parametrize("name,price,quantity,why", [
    ("", 50, 1, "blank name"),
    ("   ", 50, 1, "whitespace-only name"),
    ("apple", -1, 1, "negative price"),
    ("apple", 50, 0, "zero quantity"),
    ("apple", 50, -2, "negative quantity"),
])
def test_invalid_items_are_rejected(name, price, quantity, why):
    with pytest.raises(BasketError):
        Item(name, price, quantity)
```

pytest runs that as **five separate tests**, each named by its inputs, so a
failure tells you exactly which case broke. Run `pytest -v` and look at the
names.

The `why` column is never used by the code. It is there so the list reads as
documentation.

And one case that is easy to miss:

```python
def test_a_free_item_is_allowed():
    """Zero is a legitimate price. Only negative is nonsense."""
    assert line_total(Item("free sample", 0, 2)) == 0
```

**Zero versus negative is a boundary**, and boundaries are where bugs live. If
you had written `if not self.unit_price_pence` instead of `< 0`, this test
would catch it. Try that substitution and watch it go red.

### 1:40 to 2:00 — The checklist

Here is the thing to memorise. Given any function, ask for these. **Say this
list out loud in an interview even when you are not asked**, because it is what
separates a senior answer from a correct one:

- the normal case
- empty input
- a single item
- duplicates and ties
- malformed or wrong-typed input
- **boundaries: zero, one, and either side of every threshold**
- the error path: does it raise what it should?

Apply it to a discount function. Add this to `basket.py`:

```python
def apply_discount(amount_pence: int, percent: int) -> int:
    """Take a whole-number percentage off, rounding to the nearest penny.

    Rounds half up, because rounding a customer's money down by default is the
    sort of thing that shows up in a complaint.
    """
    if not 0 <= percent <= 100:
        raise BasketError(f"percent must be between 0 and 100: {percent}")
    discount = (amount_pence * percent + 50) // 100
    return amount_pence - discount
```

Now write the checklist out as tests:

```python
def test_no_discount_leaves_the_amount_alone():
    assert apply_discount(1000, 0) == 1000


def test_a_full_discount_makes_it_free():
    assert apply_discount(1000, 100) == 0


def test_ten_percent_off_a_round_number():
    assert apply_discount(1000, 10) == 900


def test_rounding_goes_half_up_in_the_customers_favour():
    """10% of 995 is 99.5p. Rounding up the discount gives the customer 895."""
    assert apply_discount(995, 10) == 895


def test_discounting_nothing_is_still_nothing():
    assert apply_discount(0, 25) == 0


@pytest.mark.parametrize("percent", [-1, 101, 1000])
def test_an_impossible_percentage_is_rejected(percent):
    with pytest.raises(BasketError):
        apply_discount(1000, percent)
```

**The rounding test is the one that earns its keep.** Remove the `+ 50` from
`apply_discount`, which turns round-half-up into truncation, and run pytest:

```
>       assert apply_discount(995, 10) == 895
E       assert 896 == 895
FAILED test_basket.py::test_rounding_goes_half_up_in_the_customers_favour
1 failed, 45 passed
```

A one penny error, caught automatically, on a line that looks obviously
correct. That is what tests are for. Put the `+ 50` back.

**Five minutes off.**

---

## Hour 3: testing things that touch the world

The hard part of testing is never the arithmetic. It is the clock, the
filesystem, the network and the database. The answer is always the same:
**make the awkward thing a parameter.**

### 2:00 to 2:20 — The clock

Add a time-limited voucher:

```python
@dataclass(frozen=True)
class Voucher:
    """A discount code that only works between two dates."""

    code: str
    percent: int
    valid_from: str   # ISO date, e.g. '2026-01-01'
    valid_to: str     # inclusive


def voucher_percent(code: str, vouchers, today: str) -> int:
    """How much this code is worth today. Unknown or expired codes are worth 0.

    `today` is a parameter rather than a call to date.today() inside, which is
    what lets a test check an expired voucher without waiting for time to pass.
    """
    for voucher in vouchers:
        if voucher.code == code and voucher.valid_from <= today <= voucher.valid_to:
            return voucher.percent
    return 0
```

```python
VOUCHERS = (
    Voucher("SAVE10", 10, "2026-01-01", "2026-12-31"),
    Voucher("OLD", 50, "2020-01-01", "2020-12-31"),
)


def test_a_current_voucher_is_worth_its_percentage():
    assert voucher_percent("SAVE10", VOUCHERS, "2026-06-01") == 10


def test_an_expired_voucher_is_worth_nothing():
    assert voucher_percent("OLD", VOUCHERS, "2026-06-01") == 0


def test_an_unknown_code_is_worth_nothing():
    assert voucher_percent("NOPE", VOUCHERS, "2026-06-01") == 0


def test_a_voucher_works_on_its_first_day():
    assert voucher_percent("SAVE10", VOUCHERS, "2026-01-01") == 10


def test_a_voucher_works_on_its_last_day():
    assert voucher_percent("SAVE10", VOUCHERS, "2026-12-31") == 10


def test_a_voucher_does_not_work_the_day_before_it_starts():
    assert voucher_percent("SAVE10", VOUCHERS, "2025-12-31") == 0


def test_a_voucher_does_not_work_the_day_after_it_ends():
    assert voucher_percent("SAVE10", VOUCHERS, "2027-01-01") == 0
```

**Look at those last four.** First day, last day, one day before, one day
after. Off-by-one errors in date ranges are extremely common, and only boundary
tests find them. If `voucher_percent` used `<` instead of `<=`, exactly one of
these would fail and tell you which end was wrong.

**Now imagine testing this with `date.today()` inside the function.** You could
not test the expired case at all without changing the system clock. Passing
`today` in costs one parameter and buys the entire test suite. **That is
dependency injection**, and it is the single most useful idea in testable
design.

### 2:20 to 2:45 — The filesystem

```python
def load_prices(path) -> dict:
    """Read a 'name,pence' price list, skipping blanks, comments and bad rows."""
    prices = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) != 2:
                continue
            try:
                prices[parts[0].strip()] = int(parts[1])
            except ValueError:
                continue
    return prices
```

pytest gives you a real temporary directory, cleaned up afterwards:

```python
def test_loads_a_simple_price_list(tmp_path):
    path = tmp_path / "prices.csv"
    path.write_text("apple,50\nbread,120\n", encoding="utf-8")
    assert load_prices(path) == {"apple": 50, "bread": 120}


def test_skips_blanks_and_comments(tmp_path):
    path = tmp_path / "prices.csv"
    path.write_text("# a comment\n\napple,50\n\n", encoding="utf-8")
    assert load_prices(path) == {"apple": 50}


def test_skips_malformed_rows_without_giving_up(tmp_path):
    path = tmp_path / "prices.csv"
    path.write_text("apple,50\nbroken-row\ncheese,notanumber\nbread,120\n", encoding="utf-8")
    assert load_prices(path) == {"apple": 50, "bread": 120}


def test_an_empty_file_gives_an_empty_price_list(tmp_path):
    path = tmp_path / "prices.csv"
    path.write_text("", encoding="utf-8")
    assert load_prices(path) == {}


def test_a_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_prices(tmp_path / "nope.csv")
```

**`tmp_path` is a fixture**: ask for it by name in the parameter list and
pytest supplies a fresh directory per test. No cleanup code, no shared state,
no tests interfering with each other.

Notice `test_skips_malformed_rows_without_giving_up`. Real data files contain
garbage, and the policy question, do we crash or do we skip, is a decision the
test now documents.

### 2:45 to 3:00 — Your own fixtures

```python
class Basket:
    """A basket you add to, which knows what it costs."""

    def __init__(self, prices: dict):
        self._prices = prices
        self._items: list[Item] = []

    def add(self, name: str, quantity: int = 1) -> None:
        if name not in self._prices:
            raise BasketError(f"unknown item: {name}")
        self._items.append(Item(name, self._prices[name], quantity))

    @property
    def items(self):
        return tuple(self._items)

    def total(self, code: str = "", vouchers=(), today: str = "") -> int:
        """What the customer pays, in pence, after any valid voucher."""
        gross = subtotal(self._items)
        percent = voucher_percent(code, vouchers, today) if code else 0
        return apply_discount(gross, percent)
```

`Basket` takes its price list as a constructor argument rather than loading a
file itself. Same idea again: **the awkward thing is a parameter.**

```python
@pytest.fixture
def prices():
    """The price list every basket test starts from."""
    return {"apple": 50, "bread": 120, "milk": 95}


@pytest.fixture
def basket(prices):
    """An empty basket. Fixtures can use other fixtures."""
    return Basket(prices)


def test_a_new_basket_is_empty(basket):
    assert basket.items == ()
    assert basket.total() == 0


def test_adding_several_items(basket):
    basket.add("apple", 3)
    basket.add("bread")
    assert basket.total() == 270


def test_an_unknown_item_is_rejected(basket):
    with pytest.raises(BasketError, match="unknown item"):
        basket.add("caviar")


def test_a_rejected_item_does_not_end_up_in_the_basket(basket):
    with pytest.raises(BasketError):
        basket.add("caviar")
    assert basket.items == ()


def test_a_valid_voucher_reduces_the_total(basket):
    basket.add("apple", 3)
    basket.add("bread")
    assert basket.total("SAVE10", VOUCHERS, "2026-06-01") == 243


def test_tests_do_not_leak_into_each_other(basket):
    """This basket is empty even though the test above added two items."""
    assert basket.items == ()
```

**A fixture runs fresh for every test that asks for it.** That last test proves
it, and that property is what makes a suite trustworthy: **a test that only
passes when another ran first is worse than no test**, because it fails
mysteriously months later.

`test_a_rejected_item_does_not_end_up_in_the_basket` is worth noticing too. It
tests that a failure left **no** side effect, which is a case people routinely
forget.

**Five minutes off.**

---

## Hour 4: judgement

### 3:00 to 3:20 — Test-driven development

So far you wrote code then tested it. Now reverse it. **Red, green, refactor:**

1. Write a failing test for behaviour that does not exist. Run it. **See it
   fail.**
2. Write the least code that makes it pass.
3. Tidy up, with the test protecting you.

Do it now, for a "buy two get one free" offer.

**Red:**

```python
def test_three_apples_cost_two():
    assert bogof_price(unit_price=50, quantity=3) == 100
```

```bash
pytest -q       # NameError: name 'bogof_price' is not defined
```

**Green**, the least code that passes:

```python
def bogof_price(unit_price: int, quantity: int) -> int:
    return 100
```

That is not a joke. It passes. Which tells you the test does not yet pin the
behaviour, so write the next failing test:

```python
@pytest.mark.parametrize("quantity,expected", [
    (0, 0), (1, 50), (2, 100), (3, 100), (4, 150), (6, 200), (7, 250),
])
def test_every_third_apple_is_free(quantity, expected):
    assert bogof_price(unit_price=50, quantity=quantity) == expected
```

**Green** properly:

```python
def bogof_price(unit_price: int, quantity: int) -> int:
    """Buy two, get one free: every third item costs nothing."""
    payable = quantity - quantity // 3
    return payable * unit_price
```

What TDD actually buys, and this is the honest version rather than the
evangelical one:

- **You cannot write an untestable design**, because the test exists first.
- **You see every test fail**, so you know it can fail. A test you never saw
  red might be asserting nothing.
- **You write less code**, because you stop when the tests pass.

It is not compulsory, and plenty of good engineers use it selectively. Use it
when the behaviour is well specified and fiddly, which is exactly what a
pricing rule is.

### 3:20 to 3:40 — Coverage, and why the number lies

```bash
pytest -q --cov=basket --cov-report=term-missing
```

```
Name        Stmts   Miss  Cover   Missing
basket.py      66      0   100%
TOTAL          66      0   100%
```

100%. Now prove to yourself that this means less than it looks. Write this
deliberately useless test in a file of its own:

```python
def test_everything_runs():
    """Executes a lot of lines and asserts nothing useful."""
    item = Item("apple", 50, 3)
    line_total(item)
    subtotal([item])
    apply_discount(1000, 10)
    format_pence(1234)
    assert True
```

```bash
pytest -q test_weak.py --cov=basket --cov-report=term
```

```
basket.py      66     31    53%
1 passed
```

**One test, no real assertions, and it claims to cover half the module.** Every
one of those functions could return the wrong answer and this test would still
pass.

So state it honestly, and this is the interview answer:

> **Coverage is a good detector of untested code and a bad measure of test
> quality.** It counts lines executed, not assertions made. Zero coverage on
> the pricing logic is alarming; ninety percent with assertions that cannot
> fail is worthless. I use it to find gaps and to set a floor that must not
> regress, never as a target in itself. The honest check is to break the code
> deliberately and confirm a test goes red.

Branch coverage is more informative than line coverage. **Mutation testing**
tools such as `mutmut` do the breaking automatically: they change your code in
small ways and report which mutations your tests failed to catch. That is the
real measure, when a programme will pay for it.

### 3:40 to 3:52 — Doubles, and the one rule about them

The vocabulary, which interviewers do ask you to distinguish:

| Name | What it is |
| --- | --- |
| **Dummy** | Filler to satisfy a signature, never used |
| **Stub** | Returns canned answers |
| **Spy** | A stub that also records how it was called |
| **Mock** | Pre-programmed with expectations; you assert on the interaction |
| **Fake** | A real but simplified implementation |

Everything you have written this sprint used **fakes**: a dict of prices
instead of a database, a tuple of vouchers instead of a service, `tmp_path`
instead of a real data directory. That is deliberate.

Here is a mock, for comparison:

```python
from unittest.mock import MagicMock

def test_checkout_notifies_the_customer():
    notifier = MagicMock()
    checkout(basket, notifier=notifier)
    notifier.send.assert_called_once()
```

**Prefer fakes to mocks, and be ready to say why:** a test that asserts on a
chain of mock interactions breaks whenever you restructure the code, even when
the behaviour is unchanged. A test against a fake asserts on outcomes and
survives refactoring.

And the deeper point, which is the single best sentence you can offer on this
topic:

> **If a class is hard to test, that is a design defect, not a testing
> problem.** Hard to test almost always means it builds its own dependencies,
> reads global state, or does several unrelated things.

### 3:52 to 4:00 — Self-test

From memory, write:

1. A test that a function raises `ValueError` on bad input, checking the
   message.
2. A parametrised test with four cases.
3. A fixture, and a test that uses it.
4. The seven-item checklist of what to test.
5. One sentence on what coverage does and does not tell you.
6. One sentence on why you would inject a clock.

## What you can honestly claim

**Say:** you write pytest suites including parametrised cases, exception tests
and fixtures; you test boundaries and error paths rather than just the happy
path; you design for testability by injecting clocks, paths and collaborators;
you can work test-first; and you read coverage honestly.

That is a genuine, defensible skill set, and it is precisely what the posting
asks for.

## If you get another four hours

1. **[Lesson 19](testing-ci.html)**: the pyramid, flaky tests, and CI gates.
2. **The [practice repo](../practice/README.html)**: 84 Python tests to read,
   and stubs to fill in with `PREP_TARGET=exercises pytest -q`.
3. **Add characterization tests** to something you did not write: capture what
   it does today, then refactor safely behind them.
4. **Install `mutmut`** and run it against `basket.py`. Fix what it finds.
5. **Wire the suite into CI**, per [lesson 9](sdlc-sprint.html).
