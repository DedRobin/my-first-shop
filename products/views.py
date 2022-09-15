from django.shortcuts import render, redirect

from products.forms import PurchaseForm
from products.models import Product, FavoriteProduct, Purchase
from products.services import get_sorted_product
from users.models import User


def index(request):
    return redirect("products")


def products(request):
    form = PurchaseForm()
    product_list = Product.objects.order_by("id")

    order_by = request.GET.get("order_by")
    product_list = get_sorted_product(queryset=product_list, order_by=order_by)
    product_list = product_list.all()[:24]

    user_list = User.objects.all()  # По Purchase отловить User

    if request.user.is_authenticated:
        favorite_count = Product.objects.filter(favorites__user=request.user).count()
        return render(request, "index.html", {"product_list": product_list,
                                              "user_list": user_list,
                                              "form": form,
                                              "favorite_count": favorite_count})
    else:
        return render(request, "index.html", {"product_list": product_list,
                                              "user_list": user_list,
                                              "form": form})


def favorites(request):
    if request.user.is_authenticated:
        form = PurchaseForm()
        favorite_list = Product.objects.filter(favorites__user=request.user)
        return render(request, "index.html", {"product_list": favorite_list,
                                              "favorite_count": favorite_list.count(),
                                              "form": form})
    else:
        return redirect("index")


def as_favorite(request, product_id):
    if request.user.is_authenticated:

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


def purchases(request):
    if request.user.is_authenticated:
        purchase_list = Purchase.objects.filter(user=request.user)
        favorite_count = Product.objects.filter(favorites__user=request.user).count()
        return render(request, "purchases.html", {"purchase_list": purchase_list,
                                                  "favorite_count": favorite_count})
    else:
        return redirect("index")
