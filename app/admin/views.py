from starlette_admin.contrib.sqla import ModelView
from starlette_admin import DropDown
from starlette_admin.fields import TextAreaField

from app.models import Suite, Collection, Item, Package, Testimonial


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


class PackageView(ModelView):
    """
    Admin view for Package management
    """

    label = "Packages"
    icon = "fa fa-folder"
    fields = [
        "id",
        "name",
        "price",
        "description",
        TextAreaField(
            "features",
            label="Features",
            help_text="Enter features, one per line",
        ),
        "pdf_url",
        "is_active",
        "is_popular",
        "created_at",
        "updated_at",
        "display_order",
    ]
    searchable_fields = ["name", "description"]
    sortable_fields = ["name", "display_order", "created_at"]


class TestimonialView(ModelView):
    """
    Admin view for Testimonial management
    """

    label = "Testimonials"
    icon = "fa fa-comment"
    fields = [
        "id",
        "client_name",
        "review_text",
        "rating",
        "created_at",
        "updated_at",
        "display_order",
    ]
    searchable_fields = ["client_name", "review_text"]
    sortable_fields = ["client_name", "created_at"]


def setup_admin_views(admin):
    """
    Setup all admin views for your models
    """
    admin.add_view(
        DropDown(
            "Product Management",
            icon="fa fa-tshirt",
            views=[
                SuiteView(Suite),
                CollectionView(Collection),
                ItemView(Item),
                PackageView(Package),
                TestimonialView(Testimonial),
            ],
        )
    )
