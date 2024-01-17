import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


# Function to parse the domain from a URL
def get_domain(url):
    try:
        parsed_uri = urlparse(url)
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    except Exception as e:
        print(f"Error parsing URL '{url}': {e}")
        return None


# Function to perform an HTTP GET request
def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad HTTP status
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching '{url}': {e}")
        return None


# Function to parse the HTML content of the website
def parse_website_content(url, content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        hyperlinks = [a.get('href') for a in soup.find_all('a', href=True)]
        external_resources_script = [script['src'] for script in soup.find_all('script', src=True)]
        external_resources_img = [img['src'] for img in soup.find_all('img', {'height': '1', 'width': '1'})]

        base_domain = get_domain(url)
        third_party_resources_script = [url for url in external_resources_script if get_domain(url) != base_domain]
        third_party_resources_img = [url for url in external_resources_img if get_domain(url) != base_domain]

        return hyperlinks, external_resources_script, external_resources_img, third_party_resources_script, third_party_resources_img
    except Exception as e:
        print(f"Error parsing content from '{url}': {e}")
        return [], [], [], [], []


# Function to initialize WebDriver for Selenium
def initialize_webdriver():
    try:
        driver = webdriver.Chrome()
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None


def web_analyzer(url):
    content = fetch_website_content(url)
    if content:
        hyperlinks, external_resources_script, external_resources_img, third_party_resources_script, third_party_resources_img = parse_website_content(
            url, content)

        dynamic_pixel_srcs = []

        driver = initialize_webdriver()
        if driver:
            driver.get(url)
            dynamic_pixel_srcs = [img.get_attribute('src') for img in driver.find_elements(By.TAG_NAME, 'img')
                                  if img.get_attribute('height') == '1' and img.get_attribute('width') == '1']
            driver.quit()

        return (third_party_resources_script + dynamic_pixel_srcs), third_party_resources_img

    else:
        print(f"Failed to retrieve {url}")
        return [],[]


def main_aux(url, depth_counter):

    list_src, list_img = web_analyzer(url)

    if list_img == [] and list_src == []:
        return

    full_list = list_src + list_img

    for link in full_list:
        print(link)
        main_aux(link, depth_counter + 1)

    with open('tracking_pixels.csv', newline='') as csvfile:
        # Create a CSV reader object
        csvreader = csv.reader(csvfile)

        # Skip the header row if your CSV has one
        next(csvreader)

        # Iterate over each row in the CSV
        with open('tracking_pixels.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Resource Type', 'Tracking Pixel URL', 'depth'])
            for url in list_src:
                writer.writerow(['Script', url, depth_counter])
            for url in list_img:
                writer.writerow(['Image', url, depth_counter])


def main():
    open('your_file.csv', 'w', newline='')
    url = 'https://www.airbnb.com'
    main_aux(url, 0)


if __name__ == '__main__':
    main()
