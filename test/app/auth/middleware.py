from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from app.auth.auth_handler import decode_token

class AuthMiddleware:
    def __init__(self, app):
        self.app = app
        self.security = HTTPBearer()

    async def __call__(self, request: Request, call_next):
        if request.url.path in ["/", "/api/auth/signup", "/api/auth/login"]:
            return await call_next(request)

        try:
            credentials = await self.security(request)
            token = credentials.credentials
            payload = decode_token(token)
            request.state.user = payload.username
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
        
        response = await call_next(request)
        return response