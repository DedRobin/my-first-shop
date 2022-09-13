from django.shortcuts import render, redirect

from products.models import Product, FavoriteProduct
from users.models import User


def products(request):
    email = "Not login"
    if request.user.is_authenticated:
        email = request.user.email

    product_list = Product.objects.order_by("id").all()[:24]
    return render(request, "index.html", {"product_list": product_list, "email": email})


def as_favorite(request, product_id):
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)

        record_exists = FavoriteProduct.objects.filter(user=user, product_id=product_id).exists()

        if record_exists:
            FavoriteProduct.objects.filter(user=user, product_id=product_id).delete()
        else:
            FavoriteProduct.objects.create(user=user, product_id=product_id)

    return redirect("/")
