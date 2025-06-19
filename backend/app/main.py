from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from .database import init_database, get_random_persona, add_custom_persona, get_all_personas, delete_persona
from .chat_service import ChatService
from .models import (
    PersonaResponse, 
    CustomPersonaRequest, 
    ChatRequest, 
    ChatResponse, 
    ErrorResponse,
    ChatMode
)

# Load environment variables
load_dotenv()

# Initialize chat service
chat_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global chat_service
    await init_database()
    try:
        chat_service = ChatService()
    except ValueError as e:
        print(f"Warning: {e}")
        print("Chat functionality will be limited without GROQ_API_KEY")
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Faceless Agent API",
    description="A persona-shifting AI chat agent powered by Groq and LangChain",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Faceless Agent API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "groq_configured": chat_service is not None}

@app.get("/generate_persona", response_model=PersonaResponse)
async def generate_persona():
    """Generate a random persona from the database."""
    try:
        persona = await get_random_persona()
        if not persona:
            raise HTTPException(status_code=404, detail="No personas found")
        return PersonaResponse(**persona)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating persona: {str(e)}")

@app.get("/personas", response_model=list[PersonaResponse])
async def list_personas():
    """Get all personas from the database."""
    try:
        personas = await get_all_personas()
        return [PersonaResponse(**persona) for persona in personas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching personas: {str(e)}")

@app.post("/add_persona", response_model=PersonaResponse)
async def add_persona(request: CustomPersonaRequest):
    """Add a custom persona to the database."""
    try:
        # Validate persona description
        if not chat_service or not chat_service.validate_persona(request.description):
            raise HTTPException(
                status_code=400, 
                detail="Invalid persona description. Must be at least 10 characters and appropriate content."
            )
        
        persona = await add_custom_persona(request.description)
        return PersonaResponse(**persona)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding persona: {str(e)}")

@app.delete("/personas/{persona_id}")
async def delete_persona_endpoint(persona_id: int):
    """Delete a custom persona from the database."""
    try:
        success = await delete_persona(persona_id)
        if not success:
            raise HTTPException(
                status_code=404, 
                detail="Persona not found or cannot be deleted (only custom personas can be deleted)"
            )
        return {"message": "Persona deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting persona: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Generate a chat response using the specified persona and mode."""
    try:
        if not chat_service:
            raise HTTPException(
                status_code=503, 
                detail="Chat service unavailable. Please configure GROQ_API_KEY."
            )
        
        # Validate inputs
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if not request.persona.strip():
            raise HTTPException(status_code=400, detail="Persona cannot be empty")
        
        # Generate response
        response_text, filtered = await chat_service.generate_response(
            user_input=request.message,
            persona=request.persona,
            mode=request.mode,
            conversation_history=request.conversation_history or []
        )
        
        return ChatResponse(
            response=response_text,
            persona=request.persona,
            mode=request.mode.value,
            filtered=filtered
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chat response: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
