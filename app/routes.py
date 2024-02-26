from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.config import APP_DIR
from app.expenses.models import Currency

templates = Jinja2Templates(directory=APP_DIR / "templates")
templates.env.globals["currencies"] = Currency
templates.env.globals["datetime"] = datetime
router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "main.html")
