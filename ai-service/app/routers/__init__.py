"""Initialize routers package — registers all sub-routers."""

from fastapi import APIRouter

from app.routers.analysis import router as analysis_router
from app.routers.keywords import router as keywords_router

router = APIRouter()
router.include_router(analysis_router)
router.include_router(keywords_router)

__all__ = ["router"]

