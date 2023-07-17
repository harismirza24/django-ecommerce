from django.contrib import admin
from .models import Category, Products, OrderProduct, Order, Address


# Register your models here.
@admin.register(Category)  # it registers and also make admin panel editable
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


# admin.site.register(Products)#just to register the model
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    
    list_display = ["title", "author", "slug", "price", "in_stock", "created_by"]
    list_editable = ["price", "in_stock"]
    prepopulated_fields = {"slug": ("title",)}

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):  
    list_display = ["user", "item", "ordered"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "get_items", "ordered_date", "start_date", "ordered")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "shipping_address", "billing_address", "created_at")
