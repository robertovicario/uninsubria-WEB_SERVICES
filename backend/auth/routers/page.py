# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from packages.shared.auth import session as ses_pkg

# =========================
# Endpoints
# =========================

# FastAPI
router = APIRouter(prefix='', tags=['auth'])
templates = Jinja2Templates(directory='/app/frontend/templates')

# =========================
# Endpoints
# =========================

@router.get('/login', name='auth:page')
async def page(request: Request):

    # Redirect
    if ses_pkg.verify_session(request.cookies.get(ses_pkg.SESSION_COOKIE)):
        return RedirectResponse('/dashboard', status_code=303)

    # -------------------------

    return templates.TemplateResponse(
        'pages/auth/login.html',
        {
            'request': request,
            'config': request.app.state.CONFIG
        }
    )
