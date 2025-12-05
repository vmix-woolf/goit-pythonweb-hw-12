import pytest
from tests.db import init_test_db

@pytest.mark.asyncio
async def test_init_db():
    await init_test_db()
