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
    if 'K' in like_text:  # Handle likes in thousands (e.g., '1.1K')
        return float(like_text.replace('K', '')) * 1000
    elif like_text.isdigit():  # Handle pure numeric likes
        return int(like_text)
    return 0  # Non-numeric or empty likes default to 0


# Extract posts and their timestamps
posts = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid*="post"]')
timestamps = driver.find_elements(By.CSS_SELECTOR, 'a[data-tooltip]')

# Combine posts and likes with their corresponding timestamps
combined_data = []
num_pairs = len(timestamps) // 2  # Number of complete pairs of posts/likes

for i in range(num_pairs):
    row_timestamp = timestamps[i].get_attribute("data-tooltip")  # First timestamp for the row
    post_text = posts[2*i].text 
    like_text = process_likes(posts[2*i+1].text)


    combined_data.append({
        "timestamp": row_timestamp,
        "post_text": post_text,
        "like_text": like_text
    })

driver.quit()

# Save combined data to a CSV file
filename = f"bluesky_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)  # Use default CSV formatting
    writer.writerow(["Timestamp", "Post Text", "Like Text"])  # Header row
    for entry in combined_data:
        writer.writerow([entry["timestamp"], entry["post_text"], entry["like_text"]])

print(f"Data saved to {filename}")
