import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.routes import auth, bookings, listings, users
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(listings.router)
app.include_router(bookings.router)


@app.get("/", response_class=HTMLResponse)
async def root_overview() -> str:
    """Browser-friendly landing page; use `/api` or `/docs` for JSON/API tools."""
    return _overview_html()


@app.get("/overview", response_class=HTMLResponse)
async def overview_page() -> str:
    """Web-based system overview (same as `/`)."""
    return _overview_html()


@app.get("/api")
async def api_hello() -> dict[str, str]:
    return {"message": "Hello World", "docs": "/docs", "overview": "/overview"}


def _overview_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>UrbanRelief — Overview</title>
  <style>
    :root { --bg: #0f1419; --card: #1a2332; --text: #e7ecf3; --muted: #8b9cb3; --accent: #2dd4bf; --link: #5eead4; }
    * { box-sizing: border-box; }
    body { font-family: system-ui, Segoe UI, sans-serif; background: var(--bg); color: var(--text);
      margin: 0; line-height: 1.55; min-height: 100vh; }
    .wrap { max-width: 720px; margin: 0 auto; padding: 2rem 1.25rem; }
    h1 { font-size: 1.75rem; font-weight: 700; margin: 0 0 0.35rem; letter-spacing: -0.02em; }
    .tag { color: var(--accent); font-size: 0.9rem; font-weight: 600; }
    p.lead { color: var(--muted); margin: 0 0 1.75rem; font-size: 1rem; }
    .cards { display: grid; gap: 0.75rem; margin-bottom: 1.75rem; }
    .card { background: var(--card); border-radius: 10px; padding: 1rem 1.15rem; border: 1px solid #2a3544; }
    .card h2 { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); margin: 0 0 0.5rem; }
    .card code, .card a { font-size: 0.92rem; }
    a { color: var(--link); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .actions { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-bottom: 2rem; }
    .btn { display: inline-block; padding: 0.55rem 1rem; border-radius: 8px; font-weight: 600; font-size: 0.9rem;
      background: var(--accent); color: #042f2e; }
    .btn:hover { filter: brightness(1.08); text-decoration: none; }
    .btn.secondary { background: #334155; color: var(--text); }
    table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
    th, td { text-align: left; padding: 0.45rem 0.6rem; border-bottom: 1px solid #2a3544; }
    th { color: var(--muted); font-weight: 600; }
    footer { color: var(--muted); font-size: 0.82rem; margin-top: 2rem; }
  </style>
</head>
<body>
  <div class="wrap">
    <p class="tag">Urban living & travel</p>
    <h1>UrbanRelief</h1>
    <p class="lead">Backend overview and links to interactive API docs. Four pillars: Short-Stay, Bachelor, Family, Tourism — plus n8n automation and Flutter mobile.</p>

    <div class="actions">
      <a class="btn" href="/docs">Open Swagger UI</a>
      <a class="btn secondary" href="/redoc">Open ReDoc</a>
      <a class="btn secondary" href="/openapi.json">OpenAPI JSON</a>
      <a class="btn secondary" href="/api">JSON ping</a>
    </div>

    <div class="cards">
      <div class="card">
        <h2>Auth &amp; NID</h2>
        <code>POST /api/v1/auth/verify-nid</code> — NID upload → n8n (<code>N8N_NID_WEBHOOK</code>)
      </div>
      <div class="card">
        <h2>Search</h2>
        <code>GET /api/v1/listings/search</code> — geo radius, category, tourism filters, Bachelor compatibility, host reputation sort
      </div>
      <div class="card">
        <h2>Users &amp; profiles</h2>
        <code>POST /api/v1/users</code> · <code>GET/PATCH /api/v1/users/{id}</code> · lifestyle <code>PUT/GET …/lifestyle-profile</code>
      </div>
      <div class="card">
        <h2>Listings CRUD</h2>
        <code>POST /api/v1/listings</code> · <code>GET/PATCH /api/v1/listings/{id}</code> · tourism <code>PUT/GET …/tourism-detail</code>
      </div>
      <div class="card">
        <h2>Bookings</h2>
        <code>POST /api/v1/bookings</code> (create) · <code>GET …/summary</code> · <code>POST …/confirm</code>
      </div>
      <div class="card">
        <h2>Automation</h2>
        <code>GET /automation/n8n/ping</code> — webhook health-style check
      </div>
    </div>

    <div class="card">
      <h2>Main routes</h2>
      <table>
        <thead><tr><th>Method</th><th>Path</th><th>Note</th></tr></thead>
        <tbody>
          <tr><td>GET</td><td><a href="/">/</a></td><td>This overview (HTML)</td></tr>
          <tr><td>GET</td><td><a href="/api">/api</a></td><td>JSON hello</td></tr>
          <tr><td>POST</td><td>/api/v1/auth/verify-nid</td><td>Multipart NID + user_id</td></tr>
          <tr><td>POST</td><td>/api/v1/users</td><td>Register user</td></tr>
          <tr><td>PUT</td><td>/api/v1/users/{id}/lifestyle-profile</td><td>Bachelor matching profile</td></tr>
          <tr><td>POST</td><td>/api/v1/listings</td><td>Create listing (owner_id)</td></tr>
          <tr><td>GET</td><td>/api/v1/listings/search</td><td>lat, lon, radius_km, female_only, …</td></tr>
          <tr><td>POST</td><td>/api/v1/bookings</td><td>Create Pending booking</td></tr>
          <tr><td>GET</td><td>/api/v1/bookings/{id}/summary</td><td>Digital key when Confirmed</td></tr>
          <tr><td>POST</td><td>/api/v1/bookings/{id}/confirm</td><td>Confirm + OTP + n8n PDF</td></tr>
        </tbody>
      </table>
    </div>

    <footer>
      Mobile app: <code>mobile/</code> — set <code>API_BASE</code> to this host (e.g. <code>http://127.0.0.1:PORT</code>).
      Database: PostgreSQL + <code>alembic upgrade head</code>. Demo data: <code>python scripts/seed_demo.py</code> from <code>backend/</code>.
    </footer>
  </div>
</body>
</html>"""


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
