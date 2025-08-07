from tkinter import W
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from logic.stream_logic import avatar_status_listener, background_stream_task, send_text_to_stream, start_stream
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Global variable to track background task
background_task_running = False

async def background_task():
    """Simple background task that runs continuously"""
    global background_task_running
    background_task_running = True
    
    print("🚀 Background stream task started!")
    
    while background_task_running:
        # This is where your continuous logic would go
        print("💗 Background task heartbeat - I'm still running!")
        await background_stream_task()
        
        # Sleep for 5 seconds before next heartbeat
        await asyncio.sleep(5)
    
    print("🛑 Background stream task stopped")

async def avatar_status_task():
    """Simple background task that runs continuously"""
    global avatar_status_task_running
    avatar_status_task_running = True
    while avatar_status_task_running:
        print("💗 Avatar status task heartbeat - I'm still running!")
        await avatar_status_listener()
        await asyncio.sleep(5)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(background_task())
    asyncio.create_task(avatar_status_task())
    yield
    # Clean up logic here

# Create FastAPI instance
app = FastAPI(
    lifespan=lifespan,
    title="Twitch IA API",
    description="A basic FastAPI integration for Twitch IA project",
    version="1.0.0",
    docs_url="/",              # Serve Swagger UI at root
    redoc_url=None,            # Disable ReDoc (optional)
    openapi_url="/openapi.json",  # (default; can be changed),
    debug=True
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Twitch IA API", "status": "running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "twitch-ia-api"}


@app.post("/start-stream")
async def start_stream_endpoint():
    start_stream_object = await start_stream()
    return {"data": start_stream_object}

class SendTextRequest(BaseModel):
    text: str
    task_type: str = "chat"
@app.post("/send-text")
async def send_text_endpoint(payload: SendTextRequest):
    await send_text_to_stream(payload.text, payload.task_type)
    return {"data": "text sent"}

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
