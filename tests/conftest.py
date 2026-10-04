"""Shared pytest fixtures for the test suite."""
import copy
import pytest

import inventory as inv


@pytest.fixture(autouse=True)
def reset_inventory():
    """
    Before each test: remember the original state and the ID counter.
    After each test: restore them.

    This prevents state from leaking between tests (since `inventory`
    is a module-level list that persists for the process lifetime).
    """
    original_items = copy.deepcopy(inv.inventory)
    original_next_id = inv._next_id

    yield  # run the test here

    inv.inventory.clear()
    inv.inventory.extend(original_items)
    inv._next_id = original_next_id