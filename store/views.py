from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from .models import Products, Category, OrderProduct, Order, Address


# to show categories in every page: you must define category in settings TEMPLATES Options:"store.views.categories"
def categories(request):
   
    return {"categories": Category.objects.all()}


def all_products(request):
    products = Products.objects.filter(in_stock=True)
    return render(request, "home.html", {"products": products})


def products_detail(request, slug):
    product = get_object_or_404(Products, slug=slug)
    return render(request, "detail.html", {"product": product})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = Products.objects.filter(category=category)
    return render(request, "category.html", {"category": category, "products": product})


@login_required
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        return render(request, "order-summary.html", {"order": order})
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("/")



@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=product.slug).exists():
            order_item = OrderProduct.objects.filter(
                item=product, user=request.user, ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            # messages.info(request, "This item quantity was updated.")
            return redirect("store:order-summary")
        else:
            # messages.info(request, "This item was not in your cart")
            return redirect("store:products_detail", slug=slug)
    else:
        # messages.info(request, "You do not have an active order")
        return redirect("store:products_detail", slug=slug)


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Products, slug=slug)
    order_item, created = OrderProduct.objects.get_or_create(
        item=product, user=request.user, ordered=False
    )
    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.filter(user=request.user, ordered=False)[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            # messages.info(request, "This item quantity was updated.")
            return redirect("store:order-summary")
        else:
            order.items.add(order_item)
            # messages.info(request, "This item was added to your cart.")
            return redirect("store:order-summary")
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        # messages.info(request, "This item was added to your cart.")
        return redirect("store:order-summary")


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=product.slug).exists():
            order_item = OrderProduct.objects.filter(
                item=product, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            # messages.info(request, "This item was removed from your cart.")
            return redirect("store:order-summary")
        else:
            # messages.info(request, "This item was not in your cart")
            return redirect("store:products_detail", slug=slug)
    else:
        # messages.info(request, "You do not have an active order")
        return redirect("store:products_detail", slug=slug)


@login_required
def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            shipping_address = form.cleaned_data["shipping_address"]
            shipping_address2 = form.cleaned_data["shipping_address2"]
            shipping_country = form.cleaned_data["shipping_country"]
            shipping_zip = form.cleaned_data["shipping_zip"]
            billing_address = form.cleaned_data["billing_address"]
            billing_address2 = form.cleaned_data["billing_address2"]
            billing_country = form.cleaned_data["billing_country"]
            billing_zip = form.cleaned_data["billing_zip"]
            payment_options = form.cleaned_data["payment_option"]
            # string all info in backend:
            if Order.objects.filter(user=request.user, ordered=False):
                finalAddress = Address.objects.create(
                    user=request.user,
                    shipping_address=shipping_address,
                    shipping_address2=shipping_address2,
                    shipping_country=shipping_country,
                    shipping_zip=shipping_zip,
                    billing_address=billing_address,
                    billing_address2=billing_address2,
                    billing_country=billing_country,
                    billing_zip=billing_zip,
                    # payment_options = (payment_options),
                    created_at=timezone.now(),
                )
                order = Order.objects.get(user=request.user, ordered=False)
                orderproduct = OrderProduct.objects.get(
                    user=request.user, ordered=False
                )
                orderproduct.ordered = True
                order.ordered = True
                orderproduct.save()
                order.save()

                return redirect("/")
    else:
        form = CheckoutForm()
        if Order.objects.filter(user=request.user, ordered=False):
            return render(request, "checkout.html", {"form": form})
