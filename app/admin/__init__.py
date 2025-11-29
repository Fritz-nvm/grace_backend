# app/admin/__init__.py
from .admin_setup import admin
from .views import setup_admin_views

__all__ = ["admin", "setup_admin_views"]
