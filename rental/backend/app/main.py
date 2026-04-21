import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.routes import auth, bookings, core_listings, listings, users, verification
from app.services.automation import send_to_n8n

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Future: init DB engine, Redis, etc.
    yield
    # Future: shutdown hooks


app = FastAPI(
    title="UrbanRelief API",
    description="Urban living & travel ecosystem backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(verification.router)
app.include_router(users.router)
app.include_router(users.user_router)
app.include_router(listings.router)
app.include_router(bookings.router)
app.include_router(core_listings.router)


@app.get("/", response_class=HTMLResponse)
async def root_overview() -> str:
    """Browser dashboard: discovery UI + links to OpenAPI."""
    return _web_dashboard_html()


@app.get("/overview", response_class=HTMLResponse)
async def overview_page() -> str:
    """Same web UI as `/` (bookmark-friendly)."""
    return _web_dashboard_html()


@app.get("/api")
async def api_hello() -> dict[str, str]:
    return {"message": "Hello World", "docs": "/docs", "overview": "/overview"}


def _web_dashboard_html() -> str:
    path = Path(__file__).resolve().parent / "web" / "index.html"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        logger.warning("Missing app/web/index.html — serving minimal placeholder")
        return (
            "<!DOCTYPE html><html><head><meta charset='utf-8'><title>UrbanRelief</title></head>"
            "<body style='font-family:system-ui;padding:2rem;background:#0f1419;color:#e7ecf3'>"
            "<p>Dashboard template missing. Restore <code>app/web/index.html</code>.</p>"
            "<p><a style='color:#5eead4' href='/docs'>Open /docs</a></p></body></html>"
        )


@app.get("/automation/n8n/ping")
async def n8n_integration_placeholder() -> dict[str, str]:
    """
    Health-style ping to the first configured n8n webhook (NID, then agreement).
    """
    url = settings.n8n_nid_webhook or settings.n8n_agreement_webhook
    if not url:
        return {"status": "skipped", "detail": "N8N_NID_WEBHOOK and N8N_AGREEMENT_WEBHOOK not set"}

    result = await send_to_n8n(url, {"event": "ping", "source": "urbanrelief-api"})
    if result is None:
        return {"status": "error", "detail": "n8n unreachable or returned an error (see server logs)"}
    return {"status": "ok", "n8n_response": str(result)}
