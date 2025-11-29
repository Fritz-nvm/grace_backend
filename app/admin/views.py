# app/admin/views.py
from starlette_admin.contrib.sqla import ModelView
from starlette_admin import DropDown
from starlette_admin.fields import TextAreaField

# Import your actual models
from app.models import Suite, Collection, Item
from app.models.item import CategoryEnum  # Import your enum


class SuiteView(ModelView):
    """
    Admin view for Suite management
    """

    label = "Suites"
    icon = "fa fa-building"
    fields = [
        "id",
        "name",
        "description",
        "is_active",
        "created_at",
        "updated_at",
    ]
    searchable_fields = ["name", "description"]
    sortable_fields = ["name", "created_at"]


class CollectionView(ModelView):
    """
    Admin view for Collection management
    """

    label = "Collections"
    icon = "fa fa-folder"
    fields = [
        "id",
        "name",
        "description",
        "suite",
        "is_active",
        "display_order",
        "created_at",
        "updated_at",
    ]
    searchable_fields = ["name", "description"]
    sortable_fields = ["name", "display_order", "created_at"]


class ItemView(ModelView):
    """
    Admin view for Item management
    """

    label = "Items"
    icon = "fa fa-shirt"
    fields = [
        "id",
        "name",
        "description",
        "price",
        TextAreaField(
            "images", label="Image URLs", help_text="Enter image URLs, one per line"
        ),
        TextAreaField(
            "colors",
            label="Available Colors",
            help_text="Enter available colors, one per line",
        ),
        TextAreaField(
            "sizes",
            label="Available Sizes",
            help_text="Enter available sizes, one per line",
        ),
        "fabric",
        "fabric_composition",
        "category",
        "collection",
        "created_at",
        "updated_at",
    ]

    searchable_fields = ["name", "description", "fabric", "fabric_composition"]
    sortable_fields = ["name", "price", "created_at", "updated_at"]


def setup_admin_views(admin):
    """
    Setup all admin views for your models
    """
    # Product Management Dropdown
    admin.add_view(
        DropDown(
            "Product Management",
            icon="fa fa-tshirt",
            views=[
                SuiteView(Suite),
                CollectionView(Collection),
                ItemView(Item),
            ],
        )
    )
