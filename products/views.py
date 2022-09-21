from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.cache import cache

from products.forms import PurchaseForm, ProductsFilterForm
from products.models import Product, FavoriteProduct, Purchase
from products.services import get_sorted_product


# PAGES

def index(request):
    return redirect("products")


def products(request):
    form = PurchaseForm()  # Empty form for "Buy"(red) button
    filter_form = ProductsFilterForm(request.GET)
    favorite_product_id = []  # favorite product id list BY DEFAULT (for cache key)
    product_list = Product.objects.order_by("id")

    # ORDERING
    order_by = {"order_by": filter_form.data.get("order_by"),
                "price_from": filter_form.data.get("price_from"),
                "price_to": filter_form.data.get("price_to")}
    product_list = get_sorted_product(queryset=product_list,
                                      order_by=order_by,
                                      request=request)

    # PAGINATION
    page_number = request.GET.get("page", 1)
    paginator = Paginator(product_list, 15)
    page = paginator.get_page(page_number)

    # CONDITION CHOICE BY AUTHENTICATION
    if request.user.is_authenticated:
        purchase_list = Purchase.objects.all()
        favorite_product_list = Product.objects.filter(favorites__user=request.user)
        response = render(request, "index.html", {"page": page,
                                                  "form": form,
                                                  "filter_form": filter_form,
                                                  "favorite_product_list": favorite_product_list,
                                                  "purchase_list": purchase_list
                                                  })
        favorite_product_id = [x.id for x in favorite_product_list]  # get all product id from each ProductQuerySet

    else:
        response = render(request, "index.html", {"page": page,
                                                  "form": form,
                                                  "filter_form": filter_form
                                                  })

    # CACHE
    cache_key = f"products-view.filter={request.user}.{order_by}." \
                f"page={page_number}." \
                f"favorite_product_id={favorite_product_id}"
    result = cache.get(cache_key)  # get cache
    if result is not None:
        return result
    cache.set(cache_key, response, 60 * 60)

    return response


def purchases(request):
    if request.user.is_authenticated:
        purchase_list = Purchase.objects.filter(user=request.user)
        favorite_count = Product.objects.filter(favorites__user=request.user).count()
        return render(request, "purchases.html", {"purchase_list": purchase_list,
                                                  "favorite_count": favorite_count})
    else:
        return redirect("index")


# ACTIONS

def as_favorite(request):
    if request.user.is_authenticated:
        product_id = request.POST.get("product_id")
        record_exists = FavoriteProduct.objects.filter(user=request.user, product_id=product_id).exists()

        if record_exists:
            FavoriteProduct.objects.filter(user=request.user, product_id=product_id).delete()
        else:
            FavoriteProduct.objects.create(user=request.user, product_id=product_id)

    return redirect("products")


def buy_product(request, product_id):
    if request.user.is_authenticated:
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = Purchase(
                user=request.user,
                product_id=product_id,
                count=form.cleaned_data["count"])
            purchase.save()
    return redirect("index")
