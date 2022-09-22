from django.core.management.base import BaseCommand

from products.services import run_ram_spider


class Command(BaseCommand):
    help = "Crawl RAM catalog"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            type=bool,
            help='Delete all records in product table',
        )

    def handle(self, *args, **options):
        clear = options.get("--clear")
        run_ram_spider.delay(clear)
