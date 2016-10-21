import scrapy

class WikiSpider(scrapy.Spider):
     name = "quotes"
     start_urls = [
        'https://en.wikipedia.org/wiki/People%27s_Crusade',
    ]
     def parse(self, response):
        for category in response.css('div.catlinks'):
            yield {
                'title': category.css('span.text::text').extract_first(),
                'author': category.css('span small::text').extract_first(),
                'tags': category.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)