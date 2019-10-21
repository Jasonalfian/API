import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher

import json
from urllib.parse import urlparse

import http.server
from http.server import HTTPServer, SimpleHTTPRequestHandler
import base64


#spider untuk crawling data
class CoinSpider(scrapy.Spider):
    name = "coin"

    def start_requests(self):
        #menentukan url yang akan discrape
        url = "https://coinmarketcap.com/all/views/all/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.css("tbody tr"):

            #atribut yang di scrape dari web menggunakan css selector
            yield {
                "nama": row.css("a.currency-name-container::text").extract_first(),
                "simbol": row.css("td.col-symbol::text").extract_first(),
                "circulating_supply": row.css("td.circulating-supply span::attr(data-supply)").extract_first(),
                "harga": row.css("a.price::text").extract_first(),
                "market_cap": row.css("td.market-cap::text").extract_first(),
                "volume": row.css("a.volume::text").extract_first(),
                "movement(24H)": row.css('td[data-timespan="24h"]::text').extract_first()
            }

#otomatisasi scrappy agar tidak perlu dijalankan melalui command line

def hasilScrapy():
    hasil = []

    def crawler_results(signal, sender, item, response, spider):
        hasil.append(item)
    dispatcher.connect(crawler_results, signal=signals.item_passed)
    process = CrawlerProcess(get_project_settings())
    process.crawl(CoinSpider)
    process.start()
    return hasil

#memindahkan hasil scraping ke sebuah variabel untuk ditampilkan dalam format JSON
hasilFinal = hasilScrapy()  

#membuat server http local
class Requests(http.server.SimpleHTTPRequestHandler):
    def _html(self, message):
        
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")
    
    #method GET
    def do_GET(self):
        parse = urlparse(self.path)
        path = parse.path
        query = parse.query

        #Parameter coin untuk mendapatkan data
        if path == "/coin":
            if query == "":
                #respon apabila tidak ada masalah
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                #meng-return data dalam bentuk JSON
                self.wfile.write(json.dumps(hasilFinal).encode())
        else:
            #respon apabila terjadi error
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self._html("Error 404 Not Found"))

#menentukan port dimana localhost berjalan
port = 1000
#infinite loop server
try:
    with HTTPServer(("",port), Requests) as httpd:
        print("Serving at port ", port, "...")
        httpd.serve_forever()
#server akan berhenti apabila ada interupsi dari keyboard atau commandline diclose
except KeyboardInterrupt:
    print("stop")
    httpd.socket.close()