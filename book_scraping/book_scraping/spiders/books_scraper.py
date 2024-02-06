import scrapy


class BooksScraperSpider(scrapy.Spider):
    name = "books_scraper"
    allowed_domains = ["books.toscrape.com"]

    # Function to send initial Request
    def start_requests(self):
        # Way to send Request to the first page of the website and call parse function after receiving response
        for page_num in range(1, 10):
            page_url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"

            # Iterate through each page number
            yield scrapy.Request(url=page_url, callback=self.parse)

    def parse(self, response):
        book_name = response.xpath("//a/@title").getall()
        book_price = response.xpath(
            "//div[@class='product_price']/p[1]/text()"
        ).getall()
        book_link = response.xpath("//a[@title][@href]/@href").getall()

        for book_name, book_price, book_link in zip(book_name, book_price, book_link):
            yield {
                "Book Name": book_name,
                "Book Price": book_price,
                "Book Link": book_link,
            }
