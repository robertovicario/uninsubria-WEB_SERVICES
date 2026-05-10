# =========================
# Dependencies
# =========================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

from config.dynamic import dynamic
from routers import templates

# =========================
# Paths
# =========================

# Configurations
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), 'config'
)

# Templates & Static
TEMPLATES_PATH = os.path.join(
    os.path.dirname(__file__), 'templates'
)
STATIC_PATH = os.path.join(
    os.path.dirname(__file__), 'static'
)

# =========================
# Configurations
# =========================

with open(os.path.join(CONFIG_PATH, 'static.json')) as f:
    static = json.load(f)
CONFIG = {
    **static,
    **dynamic
}

# =========================
# FastAPI
# =========================

# FastAPI
app = FastAPI(
    title='Frontend',
    version='1.0.0'
)

# Static Files
app.mount(
    '/static',
    StaticFiles(directory=str(STATIC_PATH)),
    name='static'
)

# Routers
app.include_router(templates.router)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'OPTIONS'],
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

# Events
@app.on_event('startup')
def setup():

    # Paths
    app.state.CONFIG_PATH = CONFIG_PATH
    app.state.TEMPLATES_PATH = TEMPLATES_PATH
    app.state.STATIC_PATH = STATIC_PATH

    # Configurations
    app.state.CONFIG = CONFIG
