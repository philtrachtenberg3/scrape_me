import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the page with the listings
listings_url = 'https://swappa.com/bp/sellworld/listings'

# Fetch the content of the webpage
response = requests.get(listings_url)

# Use BeautifulSoup to parse the HTML content of the listings page
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements containing listings. You will need to update this to match the correct class or structure.
listings = soup.findAll('div', class_='listings')  # Update with correct class for listings

# Iterate through the listings to get each product URL
for listing in listings:
    # Find the 'a' tag with the URL for the product. You need to update this selector accordingly.
    product_link = listing.find('a', href=True)
    if product_link:
        product_path = product_link['href']
        # Adjust the product URL path
        product_url = urljoin(listings_url, product_path.replace('/bp/sellworld/listings', ''))
        # Make a new HTTP request to the product URL
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.text, 'html.parser')
        # Find the 'div' tag for the price in the product page
        price_div = product_soup.find('div', class_='listing_price')
        if price_div:
            price = price_div.text.strip()
        else:
            price = 'No price found'
            print(f'Could not find price for product at URL: {product_url}')
        # Assuming you can find the title in the listing page
        title = listing.find('a', {'title': True}).get('title') if listing.find('a', {'title': True}) else 'No title found'
        print(f'Title: {title}, Price: {price}')
