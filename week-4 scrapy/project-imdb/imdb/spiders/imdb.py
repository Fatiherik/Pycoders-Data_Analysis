import scrapy

from ..items import ImdbItem



class ImdbSpider(scrapy.Spider):
    name ='imdb'
    start_urls = ['https://www.imdb.com/list/ls004610270/?st_dt=&mode=detail&page=1&sort=list_order,asc&ref_=ttls_vm_dtlhttps://www.imdb.com/list/ls004610270/?st_dt=&mode=detail&page=1&sort=list_order,asc&ref_=ttls_vm_dtl']

    def parse(self, response):
        hrefs=response.css("div.lister-item-content a ::attr(href)").extract()

        for href in hrefs:# filmlerin kayitli oldugu div in adi
            url=response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_page)

        next_page =response.css("a.flat-button.lister-page-next.next-page ::attr(href)")
        if next_page:            
            url= response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_page(self,response):
        item= ImdbItem()

        film_name=response.css('div.title_wrapper h1 ::text').getall()[0].strip()
        film_date=response.css('div.subtext a::text').getall()[-1].split('(')[0].strip()
        film_country= response.css('div.subtext a::text').getall()[-1].strip(')\n').split('(')[-1]
        film_rate=response.css('div.ratingValue span::text').getall()[0]
        director=response.css('div.credit_summary_item a::text').getall()[0]
        stars=response.css('div.credit_summary_item a::text').getall()[-4:-1]
        
        item['Film_Name'] = film_name
        item['Film_Date'] = film_date
        item['Film_Country'] = film_country
        item['Film_Rate'] = film_rate
        item['Director'] = director
        item['Stars'] = stars

        yield item