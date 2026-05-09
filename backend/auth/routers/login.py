# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse
import json

from packages.shared.auth import session as ses_pkg

# =========================
# Endpoints
# =========================

# FastAPI
router = APIRouter(prefix='/auth/api', tags=['auth'])

# =========================
# Endpoints
# =========================

@router.post('/login', name='auth:api:login')
async def login(request: Request, response: Response):

    # Request
    data = await request.json()
    email = data.get('email')
    password = data.get('password')
    remember_me = bool(data.get('remember_me'))

    # Users
    with open(request.app.state.DB_PATH, 'r') as f:
        users = json.load(f)['users']

    # Validation
    for user in users:
        if (
            email == user['email']
            and
            ses_pkg.check_password(password, user['password'])
        ):
            max_age = ses_pkg.REMEMBER_SESSION_MAX_AGE if remember_me else ses_pkg.SESSION_MAX_AGE
            token = ses_pkg.create_session(user['email'], max_age)
            response.set_cookie(
                key=ses_pkg.SESSION_COOKIE,
                value=token,
                max_age=max_age,
                httponly=True,
                secure=ses_pkg.SESSION_COOKIE_SECURE,
                samesite='lax'
            )
            return {
                'success': True,
                'user': { 'email': user['email'] }
            }

    # -------------------------

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {
        'success': False
    }

@router.get('/logout', name='auth:api:logout')
def logout():

    # Redirect
    response = RedirectResponse(
        '/login',
        status_code=303
    )
    response.delete_cookie(
        key=ses_pkg.SESSION_COOKIE,
        path='/'
    )

    # -------------------------

    return response
