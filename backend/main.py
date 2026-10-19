from fastapi import FastAPI

app = FastAPI(
    title="FormAI Rehab API",
    description="Backend API for the FormAI Rehab rehabilitation monitoring platform",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "FormAI Rehab API is running"
    }