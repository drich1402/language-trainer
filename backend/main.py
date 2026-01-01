from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from pathlib import Path
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
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")
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
    origin = request.headers.get("origin")
    
    # Handle preflight requests
    if request.method == "OPTIONS":
        response = JSONResponse(content={})
        if origin in cors_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"
        return response
    
    response = await call_next(request)
    if origin in cors_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Include routers
app.include_router(auth.router)
app.include_router(vocab.router)

# Health check endpoint (before static files)
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# API info endpoint
@app.get("/api")
async def api_root():
    return {
        "message": "German-Spanish Vocabulary Trainer API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Mount static files (for production deployment with built frontend)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")
    
    # Serve index.html for SPA routes
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't serve static files for API routes
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return {"error": "Not found"}
        
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "Frontend not built"}
else:
    # Development mode without static files
    @app.get("/")
    async def root():
        return {
            "message": "German-Spanish Vocabulary Trainer API",
            "version": "1.0.0",
            "docs": "/docs"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
