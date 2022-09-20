import requests

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum, F, QuerySet
from shutil import copyfileobj


def get_sorted_product(queryset: QuerySet, order_by: list, request: WSGIRequest) -> QuerySet:
    if order_by == "favorite":
        return queryset.filter(favorites__user=request.user)
    if "cost" in order_by:
        queryset = queryset.order_by("cost")
    elif "-cost" in order_by:
        queryset = queryset.order_by("-cost")
    if "sold" in order_by:
        queryset = queryset.annotate(sold=Sum(F("cost") * F("purchases__count")))
        queryset = queryset.order_by("sold")
    elif "-sold" in order_by:
        queryset = queryset.annotate(sold=Sum(F("cost") * F("purchases__count")))
        queryset = queryset.order_by("-sold")
    if "popular" in order_by:
        queryset = queryset.annotate(popular=Sum("purchases__count"))
        queryset = queryset.order_by("popular")
    elif "-popular" in order_by:
        queryset = queryset.annotate(popular=Sum("purchases__count"))
        queryset = queryset.order_by("-popular")

    return queryset


def download_image_and_get_filename(url: str) -> str:
    response = requests.get(url, stream=True)
    filename = url.split("/")[-1]

    if response.status_code == 200:
        response.raw.decode_content = True
        with open(f'media/products/{filename}', 'wb') as f:
            copyfileobj(response.raw, f)

    return filename
