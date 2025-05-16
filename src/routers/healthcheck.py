from fastapi import APIRouter
from starlette.responses import JSONResponse


healthcheck_router = APIRouter()


@healthcheck_router.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})
