from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
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
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid*="post"]'))
    )
    print("Posts loaded successfully.")
except Exception as e:
    print("Failed to load posts:", e)
    driver.quit()
    exit()

# Extract posts
posts = []
post_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid*="post"]')
for post in post_elements:
    posts.append(post.text)

driver.quit()

# Get the current timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Save posts to a CSV file
filename = f"bluesky_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Post"])  # Header row
    for post in posts:
        writer.writerow([timestamp, post])

print(f"Data saved to {filename}")
