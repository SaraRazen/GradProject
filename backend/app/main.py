from fastapi import FastAPI

from app.api import auth
from app.api import exercises
from app.api import patients
from app.api import sessions


app = FastAPI(
    title="FormAI Rehab API",
    description=(
        "Backend API for the FormAI Rehab "
        "rehabilitation monitoring platform"
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# API Routers
# ---------------------------------------------------------

app.include_router(auth.router)
app.include_router(exercises.router)
app.include_router(sessions.router)
app.include_router(patients.router)