import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import json

with open("config.json", "r") as file:
    data = json.load(file)
# 🔑 Optional login (you can also log in manually if you want)
USERNAME = data["USERNAME"]
PASSWORD = data["PASSWORD"]

# Set your own path to ChromeDriver
chromedriver_path = data["CHROME_DRIVER"]
# 👤 Dedicated profile folder to store cookies & session
profile_path = data["PROFILE_PATH"] 
print(USERNAME,PASSWORD,chromedriver_path,profile_path)
service = Service(executable_path=chromedriver_path)

 # Create this folder manually once
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# 🌐 Load Instagram
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)

# Try login if fields are present
try:
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    print("🔐 Logging in...")
    time.sleep(10)
except:
    print("✅ Possibly already logged in manually or session is active.")

# ⏳ Give time to complete 2FA manually if required
print("⌛ You can now perform manual login or 2FA in the opened browser.")
print("🚀 Once logged in, DO NOT CLOSE BROWSER IMMEDIATELY. Wait a few seconds.")
input("🔑 Press Enter here when you're fully logged in and ready to save session...")

driver.quit()
print("✅ Profile saved. You can reuse this session anytime using the same profile path!")
