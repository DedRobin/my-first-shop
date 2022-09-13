from django.shortcuts import render

from products.models import Product


def products(request):
    email = "Not login"
    if request.user.is_authenticated:
        email = request.user.email

    product_list = Product.objects.order_by("id").all()[:24]
    return render(request, "index.html", {"product_list": product_list, "email": email})
