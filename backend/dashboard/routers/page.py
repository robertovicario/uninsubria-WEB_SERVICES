# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from packages.shared.auth import session as ses_pkg

# =========================
# Configurations
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
    template = 'pages/dashboard/page.html'

    # -------------------------

    # User
    user = ses_pkg.verify_session(request.cookies.get(ses_pkg.SESSION_COOKIE))
    if not user:
        return RedirectResponse(
            '/login', status_code=302
        )

    # -------------------------

    return templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.app.state.CONFIG
        }
    )
