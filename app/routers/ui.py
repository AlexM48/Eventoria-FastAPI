from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# ← создаём router для UI страниц
router = APIRouter(
    prefix="/ui",
    tags=["UI"]
)

# ← подключаем templates
templates = Jinja2Templates(directory="app/templates")


# ← страница регистрации
@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


# ← страница логина
@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


# ← страница событий
@router.get("/events")
async def events_page(request: Request):
    return templates.TemplateResponse(
        "events.html",
        {"request": request}
    )
