from fastapi import APIRouter, Request
from jinja2_fragments.fastapi import Jinja2Blocks

from app.config import APP_DIR

templates = Jinja2Blocks(directory=APP_DIR / "templates")
router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("shared/_base.html", {"request": request})