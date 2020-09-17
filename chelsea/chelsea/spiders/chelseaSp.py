import scrapy

from chelsea.chelsea.items import Post

class ChelseaspSpider(scrapy.Spider):
    name = 'chelseaSp'
    allowed_domains = ['www.reddit.com']
    start_urls = ['http://api.proxiesapi.com/?auth_key=9c4a0688929ee49ad840e66a50557d7e_sr98766_ooPq87&url=https://www.reddit.com/r/chelseafc/']
    #start_urls = ['http://api.proxiesapi.com/?auth_key=9c4a0688929ee49ad840e66a50557d7e_sr98766_ooPq87&url=https://www.reddit.com/r/chelseafc/comments/ishbbv/klopp_barks_and_lampard_goes_by/']

    custom_settings = {
        'DEPTH_LIMIT': 1
    }


    def parse(self, response):

        cards = response.xpath('//div[@class="_1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3 "]').extract()

        for card in cards:
            load = Post()
            Post['titles'] = response.css('._eYtD2XCVieq6emjKBH3m::text').extract()
            Post['votes'] = response.css('._1rZYMD_4xY3gRcSS3p8ODO::text').extract()
            Post['comments'] = response.css('.FHCV02u6Cp2zYL0fhQPsO::text').extract()
            Post['URL'] = response.xpath('//div[@class="y8HYJ-y_lTUHkQIc1mdCq _2INHSNB8V5eaWp4P0rY_mE"]//@href').extract()
            #URL = 'http://api.proxiesapi.com/?auth_key=9c4a0688929ee49ad840e66a50557d7e_sr98766_ooPq87&url=https://' + URL[0]
            # Give the extracted content row wise
            # for item in zip(titles, votes, comments, URL):
            #     # create a dictionary to store the scraped info
            #     splitted = item[2].split()
            #     number_comments = splitted[0]
            #     link = 'www.reddit.com' + item[3]
            #     PostItem = {
            #         'title': item[0],
            #         'vote': item[1],
            #         'comments': number_comments,  # retrieve only the number of comments
            #         'URL': link,  # need to concatenate the domain name
            #         #'next': item[4],
            #         }
            #     # yield or give the scraped info to scrapy
            yield load

                # get comments
            comments_url = 'http://api.proxiesapi.com/?auth_key=9c4a0688929ee49ad840e66a50557d7e_sr98766_ooPq87&url=https://www.reddit.com/' + Post['URL']
            #comments_url = 'www.reddit.com' + URL[0]
            #print('follow URL: %s', comments_url)
            yield scrapy.Request(comments_url, callback = self.thread_parse, dont_filter=True)


        # go to comments
        page_next = response.xpath('//link[@rel="next"]//@href').extract_first()
        if page_next:
            next_url = response.urljoin(page_next)
            #print('next one $$$', next_url)
            yield scrapy.Request(next_url, callback = self.parse)

    def thread_parse(self, response):    ##test stuff
        #print('#######comments thread#######')
        cards = response.xpath('//div[@class="entry unvoted"]')


        for card in cards:
            comments = response.xpath('//div[@class="md"]//p/text()').getall()
            #comments = ", ".join(comments)
            #print('&&&&&&&:', comments)
            for item in zip(comments):
                CommentItem = {
                    'COMMENT_TEXT': item[0],
                }
            yield CommentItem

            # thread_link = response.xpath('//div[@class="_3ndawrYzcvjHPJFYUHijfP "]//@href').getall()
            #
            # #check if we need to follow a link to continue the thread
            # if thread_link:
            #     con_thread = 'http://api.proxiesapi.com/?auth_key=9c4a0688929ee49ad840e66a50557d7e_sr98766_ooPq87&url=https://www.reddit.com/' + thread_link[0]
            #     yield scrapy.Request(con_thread, callback=self.thread_parse, dont_filter=True)