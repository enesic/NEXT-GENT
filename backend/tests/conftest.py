"""
Pytest configuration for test suite.
"""
import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)
