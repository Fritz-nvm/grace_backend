"""
CRUD operations for the application.
"""

# Import CRUD class instances
from app.crud.suite import suite
from app.crud.collection import collection
from app.crud.item import item
from app.crud.package import package
from app.crud.testimonial import testimonial


# Export CRUD instances
__all__ = ["suite", "collection", "item", "package", "testimonial"]
