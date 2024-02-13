import requests
import json
from bs4 import BeautifulSoup

# URL of the page with the listings
listings_url = 'https://swappa.com/bp/sellworld/listings'

# Read carrier list from JSON file
with open('carriers.json', 'r') as file:
    carriers = json.load(file)

# Read condition list from JSON file
with open('product_conditions.json', 'r') as file:
    product_conditions = json.load(file)

# Fetch the content of the webpage
response = requests.get(listings_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements containing listings
listings = soup.find_all('div', class_='listings')  # Update with correct class for listings

# Find the element containing condition information
condition_elements = soup.find_all('p', class_='mb-2')
# print(f'Condition elements: {condition_elements}')
# if len(condition_elements) >= 2:
#     condition_element = condition_elements[1]  # Selecting the second element
# else:
#     condition_element = None

# Extract condition and carrier information
condition = None
carrier = None

# Iterate through the listings to get each product URL and details
for listing in listings:
    # Extract product details
    title = listing.find('span', itemprop='name').text.strip() if listing.find('span', itemprop='name') else 'Title not available'
    price = listing.find('span', itemprop='price').text.strip() if listing.find('span', itemprop='price') else 'Price not available'
    for element in condition_elements:
    # Find all <span> elements within the condition element
        span_elements = element.find_all('span')
    # Check if the span elements contain condition and carrier information
    for span in span_elements:
        text = span.get_text(strip=True)
        if text.lower() in [condition.lower() for condition in product_conditions]:
            condition = text
        elif text.lower() in [carrier.lower() for carrier in carriers]:
            carrier = text
    
    # Print product details along with condition and carrier
    print(f'Title: {title}, Price: {price}, Condition: {condition}, Carrier: {carrier}')
