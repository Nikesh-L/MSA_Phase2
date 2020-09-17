# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChelseaItem(scrapy.Item):
    # define the fields for your item here like:
        # name = scrapy.Field()

    pass

class Post(scrapy.Item):
    title = scrapy.Field()
    votes = scrapy.Field()
    num_comments = scrapy.Field()
    URL = scrapy.Field()

class Comment(scrapy.Item):
    comments = scrapy.Field()