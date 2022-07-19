import json
import pickle

from scrapy.http import Request
from scrapy.spiders import Spider

from ..items import PlaceLoader


class YelpPlaces(Spider):
    name = 'YelpPlaces'
    allowed_domains = ['yelp.com']

    with open('yelp_place_scraper/yelp_urls.json', 'r') as f:
        start_urls = json.load(f)

    def parse(self, response):
        links = response.xpath('//a').xpath('@href')
        links = [link.get() for link in links if '/biz/' in link.get()]
        cleaned_links = set()
        for link in links:
            split_link = link.split("?", 1)
            cleaned_link = split_link[0]
            cleaned_link = 'https://www.yelp.com' + cleaned_link            
            cleaned_links.add(cleaned_link)

        cleaned_links = list(cleaned_links)

        for link in cleaned_links:
            yield Request(url=link, callback=self.parse_place_page)

        
    def parse_place_page(self, response):

        json_data_arr = response.xpath('//script[@type="application/ld+json"]/text()')
        json_data = None
        for json_obj in json_data_arr:
            json_data = json_data = json.loads(json_obj.get())
            if '@type' in json_data:
                if json_data.get('@type') in ['Restaurant', 'LocalBusiness']:
                    break

        if json_data is None:
            print('no json data available for {}'.format(response.url))
            return

        name = json_data['name']
        try:
            price_range = json_data['priceRange']
        except:
            price_range = ''
        phone = json_data['telephone']
        try:
            address = json_data['address']
            street_address = address['streetAddress']
            city = address['addressLocality']
            state = address['addressRegion']
            country = address['addressCountry']
            postal_code = address['postalCode']
        except:
            address = ''

        try:
            cuisine_type = json_data['servesCuisine']
        except:
            cuisine_type = ''
        rating = json_data['aggregateRating']['ratingValue']
        review_count = json_data['aggregateRating']['reviewCount']

        try:
            website = response.xpath("//a[contains(@href, 'website_link_type=website')]").get()
            website = website.replace('%3A', ':')
            website = website.replace('%2F', '/')
            website = website[website.index('url=')+4:website.index('&amp')]
            print(website)
        except:
            website = None

        place_loader = PlaceLoader()

        place_loader.add_value('name', name)
        place_loader.add_value('website', website)
        place_loader.add_value('email', '')
        place_loader.add_value('street_address', street_address)
        place_loader.add_value('city', city)
        place_loader.add_value('state', state)
        place_loader.add_value('country', country)
        place_loader.add_value('postal_code', str(postal_code))
        place_loader.add_value('price_range', str(price_range))
        place_loader.add_value('phone', str(phone))
        place_loader.add_value('cuisine_type', cuisine_type)
        place_loader.add_value('rating', float(rating))
        place_loader.add_value('review_count', int(review_count))

        place = place_loader.load_item()

        yield place
