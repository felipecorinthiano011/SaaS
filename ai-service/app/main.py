from fastapi import FastAPI

from app.routers import router

app = FastAPI(title="Resume Optimizer AI Service", version="0.2.0")
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

