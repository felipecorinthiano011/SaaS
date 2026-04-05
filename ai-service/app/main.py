from fastapi import FastAPI

from app.api.v1.routes_analysis import router as analysis_router

app = FastAPI(title="Resume Optimizer AI Service", version="0.1.0")
app.include_router(analysis_router, prefix="/api/v1", tags=["analysis"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

