# app/admin/admin_setup.py
import os
from typing import Optional
from fastapi import Request
from starlette.responses import Response
from starlette_admin import I18nConfig
from starlette_admin.contrib.sqla import Admin
from starlette_admin.auth import AuthProvider, login_not_required
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings

# Database engine for admin
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)


class SimpleAuthProvider(AuthProvider):
    """
    Simple authentication provider using settings
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        # Check against settings
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"username": username, "is_admin": True})
            return response
        return None

    async def is_authenticated(self, request) -> bool:
        """
        Check if user is authenticated
        """
        username = request.session.get("username")
        is_admin = request.session.get("is_admin", False)
        return bool(username and is_admin)

    def get_admin_user(self, request: Request) -> Optional[dict]:
        """
        Get current admin user details
        """
        username = request.session.get("username")
        if username:
            return {
                "username": username,
                # You can add more user details here if needed
            }
        return None

    @login_not_required
    async def logout(self, request: Request, response: Response) -> Response:
        """
        Handle admin logout
        """
        request.session.clear()
        return response


# Create admin instance
admin = Admin(
    async_engine,
    title="Clothing Brand Admin",
    auth_provider=SimpleAuthProvider(),
    i18n_config=I18nConfig(default_locale="en"),
    logo_url=settings.ADMIN_LOGO_URL,
    login_logo_url=settings.ADMIN_LOGIN_LOGO_URL,
)
