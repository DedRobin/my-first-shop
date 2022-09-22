from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum, F, QuerySet
from django_rq import job
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

from products.models import Product
from products.spiders import RamSpider


def get_sorted_product(queryset: QuerySet, order_by: dict, request: WSGIRequest) -> QuerySet:
    if order_by.get("order_by") == "favorite" and request.user.is_authenticated:
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


@job
def run_ram_spider(clear):
    if clear:
        Product.objects.all().delete()

    def crawler_results(signal, sender, item, response, spider):
        Product.objects.update_or_create(external_id=item["external_id"], defaults=item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(get_project_settings())
    process.crawl(RamSpider)
    process.start()
