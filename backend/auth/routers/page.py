# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from utils import security as sec

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
    if sec.verify_session(request.cookies.get(sec.SESSION_COOKIE)):
        return RedirectResponse('/dashboard', status_code=303)

    # -------------------------

    return templates.TemplateResponse(
        'pages/auth/login.html',
        {
            'request': request,
            'config': request.app.state.CONFIG
        }
    )
