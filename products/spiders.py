import scrapy

from decimal import Decimal

from products.services import download_image_and_get_filename


class RamSpider(scrapy.Spider):
    name = "ram.by"
    start_urls = ["https://ram.by/computers.html"]

    def parse(self, response, **kwargs):
        for product in response.css(".items.list-view .item"):
            external_id = product.css(".raiting-and-number-container .number::text").get()[
                          7:]  # slice a string -> "Номер: "

            try:
                cost = product.css(".price-container .price::text").get().strip()
                cost = cost.replace("руб.", "")
                cost = Decimal(cost.replace(",", "."))
            except Exception:
                cost = 0

            image = product.css(".image img::attr(data-src)").get()
            image_url = response.urljoin(image)

            filename = download_image_and_get_filename(image_url)

            data = {
                "external_id": external_id,
                "title": product.css(".title a::text").get().strip(),
                "cost": cost,
                "link": f"{product.css('.title a::attr(href)').get()}",
                "image": f"products/{filename}"
            }
            yield data

        next_page = response.css(".pages ul li:last-child a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
