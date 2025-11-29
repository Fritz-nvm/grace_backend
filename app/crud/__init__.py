"""
CRUD operations for the application.
"""

# Import CRUD class instances
from app.crud.suite import suite
from app.crud.collection import collection
from app.crud.item import item

# Export CRUD instances
__all__ = ["suite", "collection", "item"]
