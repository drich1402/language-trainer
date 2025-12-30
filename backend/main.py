from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from routers import auth, vocab

# Load environment variables
load_dotenv()

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Vocabulary Trainer API...")
    print(f"📝 CORS origins: {os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173')}")
    yield
    # Shutdown
    print("👋 Shutting down Vocabulary Trainer API...")

# Create FastAPI app
app = FastAPI(
    title="German-Spanish Vocabulary Trainer API",
    description="API for learning German-Spanish vocabulary with spaced repetition",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
cors_origins = [origin.strip() for origin in cors_origins]  # Remove any whitespace
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add middleware to ensure CORS headers on all responses including errors
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    origin = request.headers.get("origin")
    if origin in cors_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Include routers
app.include_router(auth.router)
app.include_router(vocab.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "German-Spanish Vocabulary Trainer API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
