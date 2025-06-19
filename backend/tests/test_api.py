import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import tempfile
import os

from app.main import app
from app.database import init_database

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

@pytest.fixture
async def temp_db_for_api():
    """Create a temporary database for API testing."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        temp_db_path = tmp.name
    
    # Patch the DATABASE_PATH
    with patch('app.database.DATABASE_PATH', temp_db_path):
        await init_database()
        yield temp_db_path
    
    # Cleanup
    if os.path.exists(temp_db_path):
        os.unlink(temp_db_path)

def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Faceless Agent API"
    assert data["version"] == "1.0.0"

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "groq_configured" in data

@pytest.mark.asyncio
async def test_generate_persona_endpoint(client, temp_db_for_api):
    """Test the generate persona endpoint."""
    with patch('app.database.DATABASE_PATH', temp_db_for_api):
        response = client.get("/generate_persona")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "description" in data
        assert "is_custom" in data

@pytest.mark.asyncio
async def test_list_personas_endpoint(client, temp_db_for_api):
    """Test the list personas endpoint."""
    with patch('app.database.DATABASE_PATH', temp_db_for_api):
        response = client.get("/personas")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert all("id" in persona and "description" in persona for persona in data)

@pytest.mark.asyncio
async def test_add_persona_endpoint(client, temp_db_for_api):
    """Test the add persona endpoint."""
    with patch('app.database.DATABASE_PATH', temp_db_for_api):
        # Mock the chat service validation
        with patch('app.main.chat_service') as mock_service:
            mock_service.validate_persona.return_value = True
            
            persona_data = {"description": "A test persona for API testing"}
            response = client.post("/add_persona", json=persona_data)
            assert response.status_code == 200
            data = response.json()
            assert data["description"] == persona_data["description"]
            assert data["is_custom"] is True

def test_add_persona_invalid(client):
    """Test adding an invalid persona."""
    with patch('app.main.chat_service') as mock_service:
        mock_service.validate_persona.return_value = False
        
        persona_data = {"description": "bad"}
        response = client.post("/add_persona", json=persona_data)
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_chat_endpoint_no_groq(client):
    """Test chat endpoint without Groq configuration."""
    with patch('app.main.chat_service', None):
        chat_data = {
            "message": "Hello",
            "persona": "A friendly AI",
            "mode": "regular"
        }
        response = client.post("/chat", json=chat_data)
        assert response.status_code == 503

@pytest.mark.asyncio
async def test_chat_endpoint_with_mock(client):
    """Test chat endpoint with mocked service."""
    mock_service = AsyncMock()
    mock_service.generate_response.return_value = ("Hello there!", False)
    
    with patch('app.main.chat_service', mock_service):
        chat_data = {
            "message": "Hello",
            "persona": "A friendly AI assistant",
            "mode": "regular"
        }
        response = client.post("/chat", json=chat_data)
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Hello there!"
        assert data["persona"] == "A friendly AI assistant"
        assert data["mode"] == "regular"
        assert data["filtered"] is False

def test_chat_endpoint_empty_message(client):
    """Test chat endpoint with empty message."""
    mock_service = AsyncMock()
    
    with patch('app.main.chat_service', mock_service):
        chat_data = {
            "message": "",
            "persona": "A friendly AI",
            "mode": "regular"
        }
        response = client.post("/chat", json=chat_data)
        assert response.status_code == 400

def test_chat_endpoint_empty_persona(client):
    """Test chat endpoint with empty persona."""
    mock_service = AsyncMock()
    
    with patch('app.main.chat_service', mock_service):
        chat_data = {
            "message": "Hello",
            "persona": "",
            "mode": "regular"
        }
        response = client.post("/chat", json=chat_data)
        assert response.status_code == 400
