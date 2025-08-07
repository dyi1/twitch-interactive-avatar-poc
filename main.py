from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from logic.stream_logic import start_stream

# Load environment variables from .env file
load_dotenv()


# Create FastAPI instance
app = FastAPI(
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



# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
