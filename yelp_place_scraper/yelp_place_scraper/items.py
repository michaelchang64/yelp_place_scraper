from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy import Field, Item
from scrapy.loader import ItemLoader


class Place(Item):
    # define the fields for your item here like:
    name = Field()
    website = Field()
    email = Field()
    street_address = Field()
    city = Field()
    state = Field()
    price_range = Field()
    phone = Field()
    country = Field()
    postal_code = Field()
    cuisine_type = Field()
    rating = Field()
    review_count = Field()

place_fields_required = [
    'name',
    'postal_code',
    # 'phone',
    # postalCode OR city/state requirement implemented in DropIncompletePipeline
]

class PlaceLoader(ItemLoader):
    default_item_class = Place
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
