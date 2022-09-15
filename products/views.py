from django.db.models import Count
from django.shortcuts import render, redirect

from products.forms import PurchaseForm
from products.models import Product, FavoriteProduct, Purchase
from products.services import get_sorted_product
from users.models import User


# PAGES

def index(request):
    return redirect("products")


def products(request):
    form = PurchaseForm()
    product_list = Product.objects.order_by("id")

    order_by = request.GET.get("order_by")
    product_list = get_sorted_product(queryset=product_list, order_by=order_by, request=request)
    product_list = product_list.all()[:24]

    if request.user.is_authenticated:
        purchase_list = Purchase.objects.all()
        favorite_product_list = Product.objects.filter(favorites__user=request.user)
        favorite_count = favorite_product_list.count()

        return render(request, "index.html", {"product_list": product_list,
                                              "form": form,
                                              "favorite_product_list": favorite_product_list,
                                              "favorite_count": favorite_count,
                                              "purchase_list": purchase_list})
    else:
        return render(request, "index.html", {"product_list": product_list,
                                              "form": form})


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
