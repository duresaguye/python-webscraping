import requests
from bs4 import BeautifulSoup
import json
import time

# URL of the webpage to scrape
url = 'https://www.aau.edu.et/offices/v_president-office/office-of-the-academic-vise-president/undergraduate-programs-office/undergraduate-programs/addis-ababa-university-institute-of-tecnology/electrical-and-computer-engineering/'
def fetch_url(url, retries=3, backoff_factor=0.3):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=100)  # Set timeout to 100 seconds
            response.raise_for_status()  # Check if the request was successful
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
    raise Exception(f"Failed to fetch the URL after {retries} attempts")

# Send a request to the webpage
response = fetch_url(url)

# Parse the webpage content
soup = BeautifulSoup(response.content, 'html.parser')

# Function to extract text by label
def extract_text(label, soup):
    element = soup.find(text=label)
    if element:
        return element.find_next().get_text(strip=True)
    return None

# Extract information
program_info = {
    'College/Institution': extract_text('College/Institution:', soup),
    'Department/School/Center': extract_text('Department/School/Center:', soup),
    'Program title': extract_text('Program title:', soup),
    'Program duration (in years)': extract_text('Program duration (in years):', soup),
    'Study Language': extract_text('Study Language:', soup),
    'Credits and the equivalent ECTS': extract_text('Credits and the equivalent ECTS:', soup),
    'Mode of delivery': extract_text('Mode of delivery:', soup),
    'Program Objective': extract_text('Program Objective', soup),
    'Admission requirements': extract_text('Admission requirements', soup),
    'Graduation requirement': extract_text('Graduation requirement', soup)
}

# Extract module and course information
modules = []
module_rows = soup.find_all('tr')
for row in module_rows:
    cols = row.find_all('td')
    if len(cols) >= 5:  # Adjust based on the number of columns in your table
        modules.append({
            'Module Code': cols[0].get_text(strip=True),
            'Module Name': cols[1].get_text(strip=True),
            'Course Code': cols[2].get_text(strip=True),
            'Course Name': cols[3].get_text(strip=True),
            'Module ECTS': cols[4].get_text(strip=True)
        })

# Combine all data into a single dictionary
data = {
    'Program Information': program_info,
    'Modules and Courses': modules
}

# Save the data as a JSON file
with open('program_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Data has been saved to 'program_info.json'")
