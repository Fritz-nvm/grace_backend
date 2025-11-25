from starlette_admin.contrib.sqla import Admin, ModelView
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Mount
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine

# NOTE: The models need to be defined or imported where they are used.
# Since you pass them as a dictionary, the setup function correctly accesses them.


# --- 1. Define ModelViews (reusable classes) ---
class CollectionAdmin(ModelView):
    name = "Collection"
    icon = "fa fa-shirt"
    fields = ["id", "name", "description"]


class ItemAdmin(ModelView):
    name = "Item"
    icon = "fa fa-box"
    fields = ["id", "name", "price", "collection_id"]


# --- 2. Setup Function to Configure and Return the Callable ASGI App ---
def setup_admin(engine: AsyncEngine, models: dict):
    """
    Initializes Starlette-Admin and wraps it in a callable Starlette
    ASGI application for mounting in FastAPI.
    """

    Collection = models.get("Collection")
    Item = models.get("Item")

    if not all([Collection, Item]):
        # Raise an informative error if models are missing
        raise ValueError(
            "Missing 'Collection' or 'Item' model in the 'models' dictionary passed to setup_admin."
        )

    # 1. Initialize the Admin object (This is NOT callable by itself)
    admin = Admin(
        engine,
        title="Clothing Brand Admin Dashboard",
        middlewares=[Middleware(CORSMiddleware, allow_origins=["*"])],
    )

    # Add ModelViews, associating them with the actual SQLAlchemy models
    admin.add_view(CollectionAdmin(Collection))
    admin.add_view(ItemAdmin(Item))

    # 2. Wrap Admin instance in a Starlette application for mounting (This is the callable ASGI app)
    # The Admin object is mounted at the root ("/") of this sub-application.
    admin_app = Starlette(routes=[Mount("/", app=admin)])

    # 3. Return the callable Starlette app
    return admin_app
