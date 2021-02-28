# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Example URL: http://units.tauniverse.com/?p=u&v=56
class TaunitsItem(scrapy.Item):

    cost_metal = scrapy.Field()
    cost_energy = scrapy.Field()
    health = scrapy.Field()
