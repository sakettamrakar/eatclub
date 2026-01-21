import pytest
from uuid import uuid4
from datetime import datetime
from src.dwbs.core.ledger.store.memory import InMemoryLedgerStore
from src.dwbs.core.ledger.events.types import LedgerEvent
from src.dwbs.core.exceptions import ConcurrencyError
from src.dwbs.core.contracts.mutation import MutationType

# Helper to create a dummy event
def create_dummy_event(expected_version=None):
    # LedgerEvent is abstract-ish, but Pydantic allows instantiation if fields match.
    # However, type checking might complain if we don't use a subclass or mock.
    # We'll use a subclass to be safe, or just instantiate LedgerEvent if not abstract.
    # The definition in types.py is a standard class, not ABC.
    return LedgerEvent(
        event_id=uuid4(),
        timestamp=datetime.now(),
        actor="test_user",
        mutation_type=MutationType.SNAPSHOT, # Using SNAPSHOT as a neutral type
        expected_version=expected_version
    )

def test_ledger_initial_version():
    store = InMemoryLedgerStore()
    assert store.version == 0

def test_append_increments_version():
    store = InMemoryLedgerStore()
    event = create_dummy_event()
    store.append(event)
    assert store.version == 1
    assert len(store.snapshot()) == 1

def test_optimistic_locking_success():
    store = InMemoryLedgerStore()

    # Version 0 -> 1
    event1 = create_dummy_event(expected_version=0)
    store.append(event1)
    assert store.version == 1

    # Version 1 -> 2
    event2 = create_dummy_event(expected_version=1)
    store.append(event2)
    assert store.version == 2

def test_optimistic_locking_failure_stale_read():
    store = InMemoryLedgerStore()

    # Advance to version 1
    store.append(create_dummy_event())
    assert store.version == 1

    # Try to append expecting version 0 (stale)
    stale_event = create_dummy_event(expected_version=0)

    with pytest.raises(ConcurrencyError) as excinfo:
        store.append(stale_event)

    assert "Version mismatch" in str(excinfo.value)
    assert store.version == 1  # Should not have incremented

def test_optimistic_locking_failure_future_version():
    store = InMemoryLedgerStore()

    # Try to append expecting version 5 (future)
    future_event = create_dummy_event(expected_version=5)

    with pytest.raises(ConcurrencyError):
        store.append(future_event)

    assert store.version == 0

def test_mixing_versioned_and_unversioned_events():
    store = InMemoryLedgerStore()

    # Append unversioned (Legacy/Admin)
    store.append(create_dummy_event(expected_version=None))
    assert store.version == 1

    # Append versioned
    store.append(create_dummy_event(expected_version=1))
    assert store.version == 2

    # Append unversioned again
    store.append(create_dummy_event(expected_version=None))
    assert store.version == 3
