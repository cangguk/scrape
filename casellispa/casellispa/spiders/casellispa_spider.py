import scrapy


class CasellispaSpider(scrapy.Spider):
    name = 'casellispa_spider'
    start_urls = ['https://www.casellispa.com/en/used-wood-machines/cnc/machining-center/54/']

    def parse(self, response):
        for item in response.xpath('//article/a/@href').extract():
            item_url = 'https://www.casellispa.com' + item
            yield scrapy.Request(item_url, callback=self.parse_item)

    def parse_item(self, response):
        title = response.xpath('//h1/text()').extract_first()
        year = ''
        brand = ''
        description = ''
        techdata = response.xpath('//div[@class="art__text"]/text()').extract()
        for desc in techdata:
            if desc.strip():
                description += desc
                hasyear = desc.lower().find("year")
                if  hasyear != - 1:
                    starty = desc.find(' ', hasyear)
                    if len(desc) - starty > 4:
                        year = desc[starty + 1:starty + 5]
        images = response.xpath('//div[@class="lg"]/a/@href').extract()
        photo = []
        for img in images:
            photo.append('https://www.casellispa.com' + img)
        yield {'title': title,
               'year of manufacture': year,
               'brand': brand,
               'description': description,
               'photo': photo,
               'url': response.url}
