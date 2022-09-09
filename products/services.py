import requests

from django.db.models import Sum, F, QuerySet
from shutil import copyfileobj


def get_sorted_product(queryset: QuerySet, order_by: str) -> QuerySet:
    if order_by == "cost":
        return queryset.order_by("cost")
    elif order_by == "-cost":
        return queryset.order_by("-cost")
    elif order_by == "sold":
        queryset = queryset.annotate(sold=Sum(F("cost") * F("purchases__count")))
        return queryset.order_by("sold")
    elif order_by == "popular":
        queryset = queryset.annotate(popular=Sum("purchases__count"))
        return queryset.order_by("popular")
    return queryset


def download_image_and_get_filename(url: str) -> str:
    response = requests.get(url, stream=True)
    filename = url.split("/")[-1]

    if response.status_code == 200:
        response.raw.decode_content = True
        with open(f'media/products/{filename}', 'wb') as f:
            copyfileobj(response.raw, f)

    return filename