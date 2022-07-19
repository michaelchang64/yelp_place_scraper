# Yelp Place Scraper

DISCLAIMER: I wrote this as a I worked on this scraper initially to help my sister find restaurants of interest for her job at a non-profit. I have periodically maintained the code to keep my knowledge of scrapy and selenium sharp.

## Usecase

The most apparent usecase for scraping Yelp is to extract basic establishment data, such as ratings, contact information, and location. By extension, one can also extract an establishment's emails given a website.

## Usage

### Installation

Given you are in the root directory `yelp_scraper`: `pip3 install -r requirements.txt`

### Preloading Yelp URLs

In the future, I plan on integrating the pagination step in the spider itself. For now I found that the best solution to evading CAPTCHAs and most effectively extracting the number of pages for a given location and category is to run it with a scraper written in selenium.

From root directory `yelp_scraper`:

1. `cd ./yelp_place_scraper`
2. `python ../init_urls_scraper/get_yelp_urls.py`

### Running the scrapy spider

Verify that the output file `yelp_urls.json` outputs paginated links. Then run:

`scrapy crawl YelpPlaces -o yelp_places.csv`

This will take a while to run given that Yelp has a sensitive nose for bots if the scraper requests pages too quickly. One can also check the raw `.jsonl` output from the `_output` directory.

### (Optional) Running the email extractor

`python email_extractor.py`

The output should come out in both `yelp_places_emails.csv` and `yelp_places_cleaned.json`.