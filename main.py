from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import predictions, analysis, recommendations

app = FastAPI(
    title="Snowball Deep Analytics API",
    description="A comprehensive API for student analytics, predictions, and recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(predictions.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Snowball Deep Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "predictions": "/api/v1/predict",
            "analysis": "/api/v1/analysis", 
            "recommendations": "/api/v1/recommend",
            "documentation": "/docs"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
