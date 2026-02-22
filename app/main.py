from fastapi import FastAPI, Depends
from app.routers import events, auth, ui

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



app = FastAPI(
    title="Eventoria API",
    version="1.0.0"
)

# ← подключаем папку static (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ← подключаем папку templates (HTML)
templates = Jinja2Templates(directory="app/templates")


app.include_router(events.router)
app.include_router(auth.router)
app.include_router(ui.router)


@app.get("/heals")
async def root():
    return {"status": "ok"}







