"""Test configuration for the practice repo.

When you run against your own stubs (``PREP_TARGET=exercises pytest -q``), a
function you have not written yet raises NotImplementedError. That is reported
as a skip rather than a failure so you can work through the problems a few at a
time and still read the output.

Against solutions.py this hook never fires.
"""

import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    outcome = yield
    excinfo = outcome.excinfo
    if excinfo and issubclass(excinfo[0], NotImplementedError):
        outcome.force_exception(pytest.skip.Exception(f"not implemented yet: {excinfo[1]}"))
