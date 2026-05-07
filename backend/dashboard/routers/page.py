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
router = APIRouter(prefix='/dashboard', tags=['dashboard'])
templates = Jinja2Templates(directory='/app/frontend/templates')

# =========================
# Endpoints
# =========================

@router.get('/', name='dashboard:page')
def dashboard(request: Request):

    # Template
    template = 'pages/dashboard/dashboard.html'

    # -------------------------

    # User
    user = sec.verify_session(request.cookies.get(sec.SESSION_COOKIE))
    if not user:
        return RedirectResponse(
            '/login',
            status_code=303
        )

    # -------------------------

    return templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.app.state.CONFIG
        }
    )
