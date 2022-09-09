from django.core.management.base import BaseCommand

from products.spiders import RamSpider
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

from products.models import Product


class Command(BaseCommand):
    help = "Crawl RAM catalog"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all records in product table',
        )

    def handle(self, *args, **options):
        def crawler_results(signal, sender, item, response, spider):
            Product.objects.update_or_create(external_id=item["external_id"], defaults=item)

        if options['clear']:
            Product.objects.all().delete()

        dispatcher.connect(crawler_results, signal=signals.item_scraped)

        process = CrawlerProcess(get_project_settings())
        process.crawl(RamSpider)
        process.start()
