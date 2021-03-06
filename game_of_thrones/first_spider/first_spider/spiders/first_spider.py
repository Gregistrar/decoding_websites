# https://doc.scrapy.org/en/latest/intro/tutorial.html
import scrapy


class Quotes(scrapy.Spider):
    """
    As you can see, our Spider subclasses scrapy.Spider and defines
    some attributes and methods:

    name: identifies the Spider. It must be unique within a project,
     that is, you can’t set the same name for different Spiders.

    start_requests(): must return an iterable of Requests (you can
    return a list of requests or write a generator function) which
    the Spider will begin to crawl from. Subsequent requests will be
     generated successively from these initial requests.

    parse(): a method that will be called to handle the response
    downloaded for each of the requests made. The response parameter
     is an instance of TextResponse that holds the page content and
     has further helpful methods to handle it.

    The parse() method usually parses the response, extracting the
    scraped data as dicts and also finding new URLs to follow and
    creating new requests (Request) from them.
    """
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


"""
A shortcut to the start_requests method
Instead of implementing a start_requests() method that 
generates scrapy.Request objects from URLs, you can just 
define a start_urls class attribute with a list of URLs. 
This list will then be used by the default implementation of 
start_requests() to create the initial requests for your spider:
"""
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)