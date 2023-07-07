import requests
from bs4 import BeautifulSoup
import urllib.parse
import os


def download_file(url, directory):
    # Extract the filename from the URL
    filename = os.path.basename(url)
    # Create the full path for saving the file
    filepath = os.path.join(directory, filename)
    # Send a GET request to the URL
    response = requests.get(url)
    # Save the file
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded: {filename}")


def scrape_page(url, directory):
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
                # Download the file
                download_file(parsed_url, directory)


# Set the URL of the web page you want to scrape
page_url = 'https://utec.edu.pe/defensoria-universitaria/'
# Set the directory to save the downloaded files
download_directory = './defensoria'

# Create the download directory if it doesn't exist
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Scrape the page and download the files
scrape_page(page_url, download_directory)
