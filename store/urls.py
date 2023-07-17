from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.all_products, name="all_products"),
    path("item/<slug:slug>", views.products_detail, name="products_detail"),
    path("search/<slug:category_slug>", views.category_list, name="category_list"),
    path("add-to-cart/<slug>", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<slug>", views.remove_from_cart, name="remove_from_cart"),
    path(
        "remove-single-item-from-cart/<slug>",
        views.remove_single_item_from_cart,
        name="remove-single-item-from-cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("order-summary", views.order_summary, name="order-summary"),
]
