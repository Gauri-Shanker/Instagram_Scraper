import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
# Path to your ChromeDriver
with open("config.json", "r") as file:
    data = json.load(file)

chromedriver_path = data["CHROME_DRIVER"]
service = Service(executable_path=chromedriver_path)

# Use the SAME folder where session was saved
profile_path = data["PROFILE_PATH"] 

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")

# Start Chrome with saved session
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Open Instagram--------------
driver.get("https://www.instagram.com/")
time.sleep(5)

# Check whether we're logged in by detecting the presence of the profile icon or login form
try:
    # Look for Instagram's home feed element or profile icon
    driver.find_element(By.XPATH, "//nav//img[contains(@alt, 'Profile photo')]")
    print("✅ Already logged in — session reuse successful!")
except:
    try:
        driver.find_element(By.NAME, "username")
        print("❌ Not logged in — session reuse failed. Please re-login and ensure profile is saved.")
    except:
        print("⚠️ Could not determine login state. Please check manually.")

# Keep browser open for verification------------------------

print("🔍 Enter username to Scrape its follower list...")

INSTAGRAM_USERNAME_TO_SCRAPE=str(input())

# Step 1: Open target profile
driver.get(f"https://www.instagram.com/{INSTAGRAM_USERNAME_TO_SCRAPE}/")
time.sleep(6)

conn = sqlite3.connect("f_f.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS f_f (
        follower TEXT,
        followed TEXT,
        UNIQUE(follower, followed)
    )
''')
conn.commit()

# Keep in-memory set to reduce redundant DB calls
already_saved = set()


# Step 2: Click on "Following"
try:
    following_button = driver.find_element(By.XPATH, "//a[contains(@href,'/followers')]")
    following_button.click()
    time.sleep(5)
except:
    print("❌ Could not find 'Following' button. Is the account private or name wrong?")
    driver.quit()
    exit()


# Wait to ensure modal loads
time.sleep(4)

# Find all divs inside the modal
modal = driver.find_element(By.XPATH, "//div[@role='dialog']")
scrollable_div = None

divs = modal.find_elements(By.TAG_NAME, "div")
for div in divs:
    try:
        scroll_height = driver.execute_script("return arguments[0].scrollHeight", div)
        client_height = driver.execute_script("return arguments[0].clientHeight", div)
        if scroll_height > client_height + 20:  # scrolling possible
            scrollable_div = div

            print("✅ Found scrollable div.")
            break
    except:
        continue

if scrollable_div is None:
    raise Exception("❌ Could not find scrollable following container.")

def wait_for_scroll_content(driver, scrollable_div, timeout=10):
    try:
        # Store old height
        old_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

        # Scroll down
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)

        # Wait until height increases or timeout
        WebDriverWait(driver, timeout).until(
            lambda d: driver.execute_script("return arguments[0].scrollHeight", scrollable_div) > old_height
        )
        return True
    except:
        return False  # No new content loaded (possibly reached bottom)


scroll_round = 0
max_idle_rounds = 3
idle_count = 0

while True:
    scrolled = wait_for_scroll_content(driver, scrollable_div, timeout=10)
    scroll_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    print(f"[{scroll_round}] Scroll height: {scroll_height}")

    # Extract and store usernames after each scroll
    user_elements = scrollable_div.find_elements(By.XPATH, ".//a[contains(@href, '/') and not(contains(@href, '/explore/'))]")
    
    new_usernames = []
    for elem in user_elements:
        href = elem.get_attribute("href")
        if href:
            parts = href.rstrip('/').split('/')
            username = parts[-1]
            if username and username not in already_saved:
                try:
                    cursor.execute("INSERT OR IGNORE INTO f_f (follower, followed) VALUES (?, ?)", 
                                   (username, INSTAGRAM_USERNAME_TO_SCRAPE))
                    already_saved.add(username)
                    new_usernames.append(username)
                    conn.commit()
                except Exception as e:
                    print(f"❌ DB Insert Error for {username}: {e}")

    if new_usernames:
        print(f"✅ {len(new_usernames)} new usernames saved in DB: {new_usernames}")
        conn.commit()
    else:
        print("ℹ️ No new usernames found in this round.")

    if not scrolled:
        idle_count += 1
        print(f"⚠️ No new content loaded. Idle round: {idle_count}/{max_idle_rounds}")
        if idle_count >= max_idle_rounds:
            print("✅ Scrolling completed. No more content to load.")
            break
    else:
        idle_count = 0

    scroll_round += 1
    time.sleep(2)

conn.close()
driver.quit()
print("🔒 All usernames saved incrementally and browser closed.")
