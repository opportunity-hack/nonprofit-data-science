import scrapy
import os
from bs4 import BeautifulSoup

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        # 'https://www.ywca.org/', #1
        #'https://www.azecon.org/', #2
        #"http://economicintegrity.org/", #3
        #"https://www.onecommunityfoundation.org/", #4
        #"https://positivepathsaz.org/", #5
        #"https://www.aaed.com/", #6
        #"https://www.jobpath.net/", #7
        #"https://sarsef.org/", #8
        "https://phoenix.dressforsuccess.org/",
        "https://gangplankhq.com/",
        "https://www.herowomenrising.org/",
        "https://econa-az.com/"

    ]

    allowed_domains = [
        #"www.ywca.org", #1
        "www.azecon.org", #2
        "economicintegrity.org", #3
        "www.onecommunityfoundation.org", #4
        "positivepathsaz.org", #5
        "www.aaed.com", #6
        "www.jobpath.net", #7
        "sarsef.org", #8
        "phoenix.dressforsuccess.org",
        "gangplankhq.com",
        "www.herowomenrising.org",
        "econa-az.com"
    ]

    def clean_html(self, html):
        soup = BeautifulSoup(html, "html.parser")  # create a new bs4 object from the html data loaded
        for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
            script.extract()
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def parse(self, response):
        url = response.url.split("/")[2]
        page = "%s%s" % (
            response.url.replace("https", "").replace("http", "").replace("/", "__").replace(":",""),
            response.url.split("/")[-2]
            )
        page = page.replace(url, "").replace("______", "")
        print(f"Url: {url} Page: {page}")

        # Don't do it like this, you need all of the HTML on the page instead:
        #all_text_on_page = ''.join(response.xpath("//body//text()").extract()).strip()

        # Using response.body is what you want so that BeautifulSoup can do its magic
        # If you don't do it like this javascript tags will still be there and you'll spend hours trying to debug it
        soup = BeautifulSoup(response.body, "lxml")

        # kill all script and style elements
        # https://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript
        for script in soup(["script", "style"]):
            script.extract()  # rip it out


        clean_text = soup.get_text().strip()
        #clean_text = self.clean_html(all_text_on_page)
        #print(clean_text)

        directory = url.replace(".","_")
        directory = f"site_{directory}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f'{directory}/text-{page}.txt'
        with open(filename, 'w') as f:
            f.write(clean_text)

        #next_page = response.css('a::attr(href)').get()
        #print(f"Next Page: {next_page}")
        yield from response.follow_all(css='a', callback=self.parse)
        #for href in response.css('a::attr(href)'):
        #    yield response.follow(href, callback=self.parse)