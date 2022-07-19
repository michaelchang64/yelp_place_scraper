import json

import pandas as pd
from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails import DefaultWorker
from extract_emails.browsers.requests_browser import RequestsBrowser as Browser

yelp_places_csv = 'yelp_places.csv'
yelp_places_emails_csv = 'yelp_places_emails.csv'
yelp_places_json_out = 'yelp_places_cleaned.json'

yelp_places_df = pd.read_csv(yelp_places_csv)
yelp_places_dict = yelp_places_df.to_dict(orient='records')
# print(yelp_places_dict)

browser = Browser()

for index, place in yelp_places_df.iterrows():
    url = place['website']
    if url:
        factory = Factory(website_url=url, browser=browser, depth=3, max_links_from_page=10)
        worker = DefaultWorker(factory)
        data = worker.get_data()
        emails = [site.data.get('email') for site in data]
        emails = list(set([email for sublist in emails for email in sublist]))
        yelp_places_dict[index]['email'] = emails

with open(yelp_places_json_out, 'w') as f:
    json.dump(yelp_places_dict, f)
# yelp_places_df.to_json(yelp_places_json_out)
yelp_places_df.to_csv(yelp_places_emails_csv, index=False)
