import pytest
import asyncio
import os
import tempfile
from unittest.mock import patch

from app.database import (
    init_database, 
    get_random_persona, 
    add_custom_persona, 
    get_all_personas,
    delete_persona,
    DEFAULT_PERSONAS
)

@pytest.fixture
async def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        temp_db_path = tmp.name
    
    # Patch the DATABASE_PATH
    with patch('app.database.DATABASE_PATH', temp_db_path):
        await init_database()
        yield temp_db_path
    
    # Cleanup
    if os.path.exists(temp_db_path):
        os.unlink(temp_db_path)

@pytest.mark.asyncio
async def test_init_database(temp_db):
    """Test database initialization."""
    personas = await get_all_personas()
    assert len(personas) == len(DEFAULT_PERSONAS)
    assert all(not persona['is_custom'] for persona in personas)

@pytest.mark.asyncio
async def test_get_random_persona(temp_db):
    """Test getting a random persona."""
    persona = await get_random_persona()
    assert persona is not None
    assert 'id' in persona
    assert 'description' in persona
    assert 'is_custom' in persona

@pytest.mark.asyncio
async def test_add_custom_persona(temp_db):
    """Test adding a custom persona."""
    custom_description = "A test persona for unit testing"
    persona = await add_custom_persona(custom_description)
    
    assert persona['description'] == custom_description
    assert persona['is_custom'] is True
    assert 'id' in persona

@pytest.mark.asyncio
async def test_delete_custom_persona(temp_db):
    """Test deleting a custom persona."""
    # Add a custom persona
    custom_description = "A persona to be deleted"
    persona = await add_custom_persona(custom_description)
    persona_id = persona['id']
    
    # Delete it
    success = await delete_persona(persona_id)
    assert success is True
    
    # Try to delete again (should fail)
    success = await delete_persona(persona_id)
    assert success is False

@pytest.mark.asyncio
async def test_cannot_delete_default_persona(temp_db):
    """Test that default personas cannot be deleted."""
    personas = await get_all_personas()
    default_persona = next(p for p in personas if not p['is_custom'])
    
    success = await delete_persona(default_persona['id'])
    assert success is False

@pytest.mark.asyncio
async def test_get_all_personas(temp_db):
    """Test getting all personas."""
    # Add a custom persona
    await add_custom_persona("Custom test persona")
    
    personas = await get_all_personas()
    assert len(personas) == len(DEFAULT_PERSONAS) + 1
    
    custom_personas = [p for p in personas if p['is_custom']]
    default_personas = [p for p in personas if not p['is_custom']]
    
    assert len(custom_personas) == 1
    assert len(default_personas) == len(DEFAULT_PERSONAS)
