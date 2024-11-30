from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
from datetime import datetime

# Define the search query
query = "vaccine"
url = f"https://bsky.app/search?q={query}"

# Set up the Selenium WebDriver with headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Sandbox is unnecessary for headless
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent resource limits on some systems

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(url)


# Wait for the posts to load dynamically
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-tooltip]'))
    )
    print("Posts and timestamps loaded successfully.")
except Exception as e:
    print("Failed to load posts:", e)
    driver.quit()
    exit()

def process_likes(like_text):
    """
    Converts like_text to a numeric value.
    - If it contains 'K', multiplies by 1000 and returns a float.
    - If it's numeric, returns an integer.
    - Otherwise, defaults to 0.
    """
    if 'K' in like_text:  # Handle likes in thousands (e.g., '1.1K')
        try:
            return float(like_text.replace('K', '')) * 1000
        except ValueError:
            return 0
    elif like_text.isdigit():  # Handle pure numeric likes
        return int(like_text)
    return 0  # Non-numeric or empty likes default to 0

# Extract posts and their timestamps
posts = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid*="post"]')
timestamps = driver.find_elements(By.CSS_SELECTOR, 'a[data-tooltip]')

# Combine posts and likes with their corresponding timestamps
combined_data = []
num_timestamps = len(timestamps)

i = 0  # Index to iterate over posts
while i < len(posts):
    # Assign the timestamp for this row
    row_timestamp = timestamps[i//2].get_attribute("data-tooltip") if i < 2 * num_timestamps else ""
    post_text = posts[i].text  # The post content
    print(row_timestamp)
    # Attempt to process the next element as a "like" if it's valid
    if i + 1 < len(posts) and (posts[i + 1].text.isdigit() or 'K' in posts[i + 1].text):
        like_text = process_likes(posts[i + 1].text)
        i += 1  # Skip the like row in the next iteration
    else:
        like_text = 0  # Default to 0 if no repost/like data

    # Add the processed data to the list
    combined_data.append({
        "timestamp": row_timestamp,
        "post_text": post_text,
        "like_text": int(like_text)
    })

    i += 1  # Move to the next post

driver.quit()

# Save combined data to a CSV file
filename = f"bluesky_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)  # Use default CSV formatting
    writer.writerow(["Timestamp", "Post Text", "Like Text"])  # Header row
    for entry in combined_data:
        writer.writerow([entry["timestamp"], entry["post_text"], entry["like_text"]])

print(f"Data saved to {filename}")
