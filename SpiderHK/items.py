# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderhkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # HACG
    hacg_videolink = scrapy.Field()

    # CNKI
    cnki_paperlink = scrapy.Field()
    cnki_pdflink = scrapy.Field()

    pass
