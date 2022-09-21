import requests

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum, F, QuerySet
from shutil import copyfileobj


def get_sorted_product(queryset: QuerySet, order_by: dict, request: WSGIRequest) -> QuerySet:
    if order_by.get("order_by") == "favorite":
        queryset = queryset.filter(favorites__user=request.user)
    elif order_by.get("order_by") == "cost":
        queryset = queryset.order_by("cost")
    elif order_by.get("order_by") == "-cost":
        queryset = queryset.order_by("-cost")
    elif order_by.get("order_by") == "sold":
        queryset = queryset.annotate(sold=Sum(F("cost") * F("purchases__count")))
        queryset = queryset.filter(sold__gt=0).order_by("sold")
    elif order_by.get("order_by") == "-sold":
        queryset = queryset.annotate(sold=Sum(F("cost") * F("purchases__count")))
        queryset = queryset.filter(sold__gt=0).order_by("-sold")
    elif order_by.get("order_by") == "popular":
        queryset = queryset.annotate(popular=Sum("purchases__count"))
        queryset = queryset.filter(popular__gt=0).order_by("popular")
    elif order_by.get("order_by") == "-popular":
        queryset = queryset.annotate(popular=Sum("purchases__count"))
        queryset = queryset.filter(popular__gt=0).order_by("-popular")

    price_from = order_by.get("price_from")
    if price_from:
        queryset = queryset.filter(cost__gte=price_from)

    price_to = order_by.get("price_to")
    if price_to:
        queryset = queryset.filter(cost__lte=price_to)

    return queryset


def download_image_and_get_filename(url: str) -> str:
    response = requests.get(url, stream=True)
    filename = url.split("/")[-1]

    if response.status_code == 200:
        response.raw.decode_content = True
        with open(f'media/products/{filename}', 'wb') as f:
            copyfileobj(response.raw, f)

    return filename
