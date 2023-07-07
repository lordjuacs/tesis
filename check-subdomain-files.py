import requests
from bs4 import BeautifulSoup
import urllib.parse
from retrying import retry


def check_file_exists(url):
    try:
        # Send a HEAD request to check the file existence
        response = requests.head(url)
        return response.status_code == requests.codes.ok
    except requests.exceptions.RequestException as e:
        print(f"Error checking file existence: {e}")
        return False


@retry(wait_fixed=2000, stop_max_attempt_number=3)
def scrape_website(url, result_file):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all <a> tags in the page
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                # Parse the URL to handle relative URLs
                parsed_url = urllib.parse.urljoin(url, href)
                # Check if the file is a Word or PDF document
                if parsed_url.endswith('.doc') or parsed_url.endswith('.docx') or parsed_url.endswith('.pdf'):
                    # Check if the file exists
                    if check_file_exists(parsed_url):
                        result_file.write(f"File exists: {parsed_url}\n")
    except requests.exceptions.RequestException as e:
        print(f"Error scraping website: {e}")


@retry(wait_fixed=2000, stop_max_attempt_number=3)
def crawl_website(parent_url, result_file):
    try:
        # Send a GET request to the parent URL
        response = requests.get(parent_url)
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all <a> tags in the page
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                # Parse the URL to handle relative URLs
                parsed_url = urllib.parse.urljoin(parent_url, href)
                # Check if the link is a subdomain or external link
                if parsed_url.startswith(parent_url):
                    # Scrape the subdomain
                    scrape_website(parsed_url, result_file)
    except requests.exceptions.RequestException as e:
        print(f"Error crawling website: {e}")


# Set the parent website URL
parent_website_url = 'https://utec.edu.pe/'

# Set the output file name
output_file = 'file_info.txt'

# Open the output file in write mode
with open(output_file, 'w') as result_file:
    # Scrape the parent website and check for the existence of files
    scrape_website(parent_website_url, result_file)

    # Crawl through the parent website and its subdomains
    crawl_website(parent_website_url, result_file)

print(f"File information saved to: {output_file}")
