from fastapi import FastAPI


app = FastAPI(
    title="FormAI Rehab API",
    description="Backend API for the FormAI Rehab rehabilitation monitoring platform",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "FormAI Rehab API is running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy"
    }