
# C:/JOE/TAUnits/TAUnits/spiders
# scrapy crawl TAUnit_Spider

from scrapy import Spider, Request
from TAUnits.items import TaunitsItem

class TAUnitSpider(Spider):
    
    # If I don't have this, I cannot run the line "scrapy crawl TAUnit_Spider"
    name = "TAUnit_Spider"
    
    start_urls = ["http://units.tauniverse.com/?p=u&v=56"]
    
    def parse(self, response):
    
        # Energy cost.  For Krogth at url http://units.tauniverse.com/?p=u&v=56, it will return 116664
        cost_energy = response.xpath('//b[@title="build cost in energy"]/text()').get()
        
        # Metal cost.  For Krogth at url http://units.tauniverse.com/?p=u&v=56, it will return 29489
        cost_metal = response.xpath('//b[@title="build cost in metal"]/text()').get()
        
        # Health of unit.  Example: for Krogoth at url http://units.tauniverse.com/?p=u&v=56, it will return 29918
        health = response.xpath('//span[@class="number"]/text()').getall()[1]
        
        # (!) Need to add a try-catch-exception here, in case the unit has no weapons
        # For a given unit, we need to find the links for its weapon(s), assuming it has weapons
        # For instance, for the Krogoth at url http://units.tauniverse.com/?p=u&v=56, it will return 3 weapon urls such as http://units.tauniverse.com/?p=w&v=2350 which are stored in weapon_urls
        weapon_url_prefix = 'http://units.tauniverse.com/'
        weapon_url_suffixes = response.xpath('//td[@class="combat_data_middle"]/a/@href').getall()
        weapon_urls = [weapon_url_prefix + weapon_url_suffix for weapon_url_suffix in weapon_url_suffixes]
        
        # For each weapon, open the page with details on this weapon, such a damage, range, AoE
        for weapon_url in weapon_urls:
            yield Request(url=weapon_url, callback=self.parse_weapon_page)

        # Now define an instance of "TaunitsItem" and initialize fields within this class instance
        item = TaunitsItem()
        item['cost_metal'] = cost_energy
        item['cost_energy'] = cost_energy
        item['health'] = health
        yield item
        
    # After opening each page for a unit's weapons, grab their details
    def parse_weapon_page(self, response):
        
        # Description of weapon, i.e. - "Gauss cannon"
        # response.xpath('//td[@style="padding:4px;"]/b')[0]
        
        # Metal cost for firing weapon
        # response.xpath('//td[@style="padding:4px;"]/b')[1]
        
        # Energy cost for firing weapon
        # response.xpath('//td[@style="padding:4px;"]/b')[2]
        
        # Reload rate in seconds
        reload_time = response.xpath('//td[@style="padding:4px;"]/b')[3]
        
        # Get area of effect and range of weapon
        weapon_ranges = response.xpath('//td[@style="padding-top:2px;padding-bottom:2px;"]/span/text()').getall()
        weapon_AoE = weapon_ranges[0]
        weapon_range = weapon_ranges[1]
        
        # Unique weapon ID.  If two weapons have the same ID, they will conflict and one of them will not fire properly in the game
        weapon_id = response.xpath('//td[@style="padding-left:4px;"]/span/text()').get()
        
        # If burst = 0, then ignore.  If burst > 0, then use it as a multiplier for weapon DPS (damage per second)
        burst = response.xpath('//td[@class="combat_data"]/span/text()').getall()[0]
        
        # Damange per shot
        damage = response.xpath('//td[@style="background-color:#575757;padding:4px;"]/span/text()').get()
         
 # (!) How to store results of scrapy program into an sql database so that I can do joins, filters, etc?
        