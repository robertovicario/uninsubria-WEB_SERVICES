# =========================
# Dependencies
# =========================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os

from frontend.config.dynamic import dynamic
from routers import (
    login,
    page
)

# =========================
# Paths
# =========================

# Database
DB_PATH = os.path.join(
    os.path.dirname(__file__),
    'db',
    'users.json'
)

# Configurations
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), 'frontend', 'config'
)
with open(os.path.join(CONFIG_PATH, 'static.json')) as f:
    static = json.load(f)

CONFIG = {
    **static,
    **dynamic
}

# =========================
# FastAPI
# =========================

# App
app = FastAPI(
    title=f"Authentication – {CONFIG['system']['name']}",
    description=CONFIG['system']['description'],
    version=CONFIG['system']['version']
)

# Static
app.mount(
    '/static',
    StaticFiles(directory='/app/frontend/static'),
    name='static'
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['Content-Type']
)

@app.middleware('http')
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'same-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    return response

# Routers
app.include_router(login.router)
app.include_router(page.router)

# =========================
# Events
# =========================

@app.on_event('startup')
def set_paths():
    app.state.CONFIG = CONFIG
    app.state.DB_PATH = DB_PATH
