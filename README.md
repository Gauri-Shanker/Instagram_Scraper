# Instagram Scraper

This project helps you log in to Instagram using Selenium and scrape followers/following lists while avoiding frequent login blocks using persistent sessions.

## 🔧 Requirements

- Python 3.x
- Chrome browser (latest version)
- ChromeDriver (matching your browser version): https://googlechromelabs.github.io/chrome-for-testing/
- Selenium library

<b>Install Selenium using pip:</b>
```
pip install selenium
```
## 📁 Project Structure

```
project-folder/
│
├── logintoinstagram.py          # Script to log in and create a session
├── followerlistscraper.py       # Scrapes the list of followers
├── followinglistscraper.py      # Scrapes the list of people you follow
└── README.md                    # Project documentation
```

## 🛠️ Setup Instructions
<b>1. Instagram Credentials</b>

In your <b>config.json</b> script, add your Instagram credentials:
```
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"
```
<b>2. Download ChromeDriver</b>

Download the correct version of ChromeDriver that matches your Chrome browser:
```
https://googlechromelabs.github.io/chrome-for-testing/
```

<b>3. Set ChromeDriver Path</b>

Update your script with the correct ChromeDriver path:
```
CHROME_DRIVER = "C:/Users/Lenovo/your_chrome_driver_path/chromedriver.exe"
```
<b>4. Set Chrome Profile Path</b>

Use a persistent Chrome profile to reduce login frequency and avoid being <b>blocked</b>:
```
PROFILE_PATH = "C:/Users/Lenovo/selenium_profiles/instagram_profile"
```

Make sure this folder exists before running the scripts.

## 🚀 How to Use

<b>Step 1: Log in to Instagram</b>

python logintoinstagram.py

This will open Chrome, use your session profile, and log in to Instagram automatically.

<b>Step 2: Scrape Data</b>

After logging in successfully:

<b>To scrape the followers list:</b>

python followerlistscraper.py

<b>To scrape the following list:</b>

python followinglistscraper.py

## 💡 Tips

- Dont ❌ Use Proxy
- Make sure your chromedriver.exe version exactly matches your Chrome browser version.
- Keeping your PROFILE_PATH consistent ensures smoother logins in future sessions.

## 📌 Disclaimer

This tool is intended for <b>educational and personal use only</b>.
Automating actions on Instagram may violate their Terms of Service: https://help.instagram.com/581066165581870

Use responsibly.
