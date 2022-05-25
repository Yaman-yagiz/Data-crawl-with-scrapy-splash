from gc import callbacks
import scrapy
from scrapy_splash import SplashRequest


class LaptopSpider(scrapy.Spider):
    name = 'laptops'
    #allowed_domains = ['www.mediaexpert.pl']
    start_urls = ["https://www.mediaexpert.pl/komputery-i-tablety/laptopy-i-ultrabooki/laptopy"]
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.59'}
    def parse(self, response):
        
        for link in response.css('h2.name a::attr(href)'):
            yield SplashRequest(url='https://www.mediaexpert.pl'+link.get(), headers=self.headers,callback=self.parse_product)

        next_page = 'https://www.mediaexpert.pl'+response.css('.list-pagination a::attr(href)')[1].get()
        if next_page != 'https://www.mediaexpert.pl' and next_page is not None:
            yield SplashRequest(url=next_page, headers=self.headers, callback=self.parse)

    def parse_product(self,response):
        try:
            yield {
            "brand": response.css('span.values::text').get(),
            "screen": response.css('span.attribute-values.is-regular::text').getall()[0].strip(),
            "procesor": response.css('span.attribute-values.is-regular::text').getall()[1].strip(),
            "RAM": response.css('span.attribute-values.is-regular::text').getall()[2].strip(),
            "Disk": response.css('span.attribute-values.is-regular::text').getall()[3].strip(),
            "Graphic Card": response.css('span.attribute-values.is-regular::text').getall()[4].strip(),
            "Operation System": response.css('span.attribute-values.is-regular::text').getall()[5].strip(),
            "Price(zł)": float(response.css('.main-price span.whole::text').get().replace("\u202f","."))
        }
        except:
            yield {
            "brand": response.css('span.values::text').get(),
            "screen": response.css('span.attribute-values.is-regular::text').getall()[0].strip(),
            "procesor": response.css('span.attribute-values.is-regular::text').getall()[1].strip(),
            "RAM": response.css('span.attribute-values.is-regular::text').getall()[2].strip(),
            "Disk": response.css('span.attribute-values.is-regular::text').getall()[3].strip(),
            "Graphic Card": response.css('span.attribute-values.is-regular::text').getall()[4].strip(),
            "Operation System": response.css('span.attribute-values.is-regular::text').getall()[5].strip(),
            "Price(zł)": response.css('.main-price span.whole::text').get()
        }
       

            # fetch('http://localhost:8050/render.html?url=https://www.mediaexpert.pl/komputery-i-tablety/laptopy-i-ultrabooki/laptopy')