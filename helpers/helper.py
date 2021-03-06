import feedparser
import re
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def get_region():
    """
    Returns the craigslist region relevant to user

    First tries to catch redirect of craigslist.org
    if redirect fails, asks user to input manually

    Parameters: None
    Returns string relating to craigslist region
    """
    url = 'https://craigslist.org'
    found = None
    with urllib.request.urlopen(url) as response:
        redirect = response.geturl()
        m = re.search('.*\/([a-z]+)\.craigslist\.org', redirect)
        if m:
            found = m.group(1)
            if found == 'www' or None:
                print("Region discovery failed")
                print("Please enter your local region such that")
                found = input(
                '[your region].craigslist.org goes to your local craigslist page: ')
    return found

def get_new_listings(region):
    """
    Checks local rss feed and returns urls of newest listings

    Parameters:
    region: local craigslist region ex. sfbay
    Returns list of string urls
    """
    rssfeed = 'https://' + region + '.craigslist.org/search/apa?format=rss'
    parsed = feedparser.parse(rssfeed)
    items = (parsed['items']) if parsed else []
    urls = []
    for item in items:
        urls.append(item['id'])
    return urls


def parse_url(url):
    """
    Reads craigslist url and extracts region, name, and id of listing

    Parameters:
    url: craigslist apartment listing url
    Returns string relating to craigslist region
    """
    m = re.search('.*\/([a-z]+)\/apa\/d\/([^\/]+)\/(\d+)\.html', url)
    region = m.group(1)
    name = m.group(2)
    id = m.group(3)
    return(region, name, id)


def scrape(url):
    """
    Scrapes craigslist apartment listing and returns apartment details

    Uses python library BeautifulSoup to visit the craigslist apartment listing
    provided and grab all important apartment information and returns a
    dictionary containing all of the info

    Parameters:
    url: craigslist apartment listing url
    Returns:
    content: dictionary containing apartment info
    """
    print("Scraping: " + url)
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    geo = soup.find('meta', {'name':"geo.position"})
    geo = geo["content"] if geo else None

    placename = soup.find('meta', {'name':"geo.placename"})
    placename = placename["content"] if placename else None

    title = soup.find('meta', {'property':"og:title"})
    title = title["content"] if title else None

    image = soup.find('meta', {'property':"og:image"})
    image = image["content"] if image else None

    price = soup.find('span', {'class':"price"})
    price = int(price.get_text(strip=True)[1:]) if price else None

    housing = soup.find('span', {'class':"housing"})
    housing = housing.get_text(strip=True) if housing else None

    bedrooms = None
    sqft = None
    if housing:
        if 'br' in housing:
            b = re.search('.* (\d+)br', housing)

            # Case: "1br -"
            if b is None:
                b = re.search('(\d+)br.*', housing)
            bedrooms = int(b.group(1))
        if 'ft' in housing:
            f = re.search('.* (\d+)ft', housing)

            # Case: "700ft -"
            if f is None:
                f = re.search('(\d+)ft.*', housing)
            sqft = int(f.group(1))

    address = soup.find('div', {'class':'mapaddress'})
    address = address.get_text(strip=True) if address else None

    gmaps = soup.find('p', {'class':'mapaddress'})
    gmaps = gmaps.find('a')["href"] if gmaps else None

    attrgroup = soup.find_all('p', {'class':'attrgroup'})
    attributes = None
    if attrgroup and len(attrgroup) > 1:
        attributes = attrgroup[1].get_text(strip=False)

    body = soup.find('section', {'id':'postingbody'})
    body = body.get_text(strip=False) if body else None

    date = soup.find_all('span', {'class':'housing_movein_now property_date shared-line-bubble'})
    if date:
        date = date[0]["data-date"]
        date = datetime.strptime(date, '%Y-%m-%d')
    else:
        date = None

    content = {
        'geo': geo,
        'placename': placename,
        'title': title,
        'image': image,
        'price': price,
        'housing': housing,
        'bedrooms': bedrooms,
        'sqft': sqft,
        'address': address,
        'gmaps': gmaps,
        'attributes': attributes,
        'body': body,
        'date': date,
        }

    return(content)
