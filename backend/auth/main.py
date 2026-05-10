# =========================
# Dependencies
# =========================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from routers import login

# =========================
# Paths
# =========================

# Database
DB_PATH = os.path.join(
    os.path.dirname(__file__),
    'db',
    'users.json'
)

# =========================
# FastAPI
# =========================

# App
app = FastAPI(
    title='Authentication',
    version='1.0.0'
)

# Routers
app.include_router(login.router)

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

# Events
@app.on_event('startup')
def setup():

    # Paths
    app.state.DB_PATH = DB_PATH

# Health Check
@app.get('/health')
def health():
    return {'status': 'ok'}
