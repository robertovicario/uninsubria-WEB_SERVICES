# =========================
# Dependencies
# =========================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import page

# =========================
# FastAPI
# =========================

# App
app = FastAPI(
    title='Dashboard',
    version='1.0.0'
)

# Routers
app.include_router(page.router)

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

# Health Check
@app.get('/health')
def health():
    return {'status': 'ok'}
