# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os

from packages.shared.auth import session as ses_pkg

# =========================
# Configurations
# =========================

# FastAPI
router = APIRouter(prefix='', tags=['templates'])
templates = Jinja2Templates(directory='/app/templates')

# =========================
# Endpoints
# =========================

@router.get('/', include_in_schema=False)
def index():
    return RedirectResponse('/login', status_code=302)

@router.get('/login', name='auth:page')
def login(request: Request):
    if ses_pkg.verify_session(request.cookies.get(ses_pkg.SESSION_COOKIE)):
        return RedirectResponse(
            '/dashboard', status_code=302
        )

    # -------------------------

    return templates.TemplateResponse(
        'pages/auth/login.html',
        {
            'request': request,
            'config': request.app.state.CONFIG
        }
    )

@router.get('/dashboard', name='dashboard:page')
@router.get('/dashboard/', include_in_schema=False)
def dashboard(request: Request):
    user = ses_pkg.verify_session(request.cookies.get(ses_pkg.SESSION_COOKIE))
    if not user:
        return RedirectResponse(
            '/login', status_code=302
        )

    # -------------------------

    return templates.TemplateResponse(
        'pages/dashboard/page.html',
        {
            'request': request,
            'config': request.app.state.CONFIG
        }
    )
