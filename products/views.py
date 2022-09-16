from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.cache import cache

from products.forms import PurchaseForm
from products.models import Product, FavoriteProduct, Purchase
from products.services import get_sorted_product


# PAGES

def index(request):
    return redirect("products")


def products(request):
    form = PurchaseForm()  # create form for "Buy"(red) button

    product_list = Product.objects.all()

    page_number = request.GET.get("page")
    order_by = request.GET.get("order_by")  # get value from filter
    cache_key = f"products-view.{order_by}.{page_number}"

    product_list = get_sorted_product(queryset=product_list,
                                      order_by=order_by,
                                      request=request)
    paginator = Paginator(product_list, 15)
    page = paginator.get_page(page_number)

    # result = cache.get(cache_key)
    # if result is not None:
    #     return result

    if request.user.is_authenticated:
        purchase_list = Purchase.objects.all()
        favorite_product_list = Product.objects.filter(favorites__user=request.user)
        favorite_count = favorite_product_list.count()
        response = render(request, "index.html", {"product_list": page,
                                                  "form": form,
                                                  "favorite_product_list": favorite_product_list,
                                                  "favorite_count": favorite_count,
                                                  "purchase_list": purchase_list})
        cache.set("products-view", response, 60 * 60)

        return response
    else:
        response = render(request, "index.html", {"product_list": page,
                                                  "form": form})
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

    return redirect("index")


def about(request):
    pass


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
