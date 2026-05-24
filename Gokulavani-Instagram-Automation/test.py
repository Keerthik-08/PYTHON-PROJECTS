from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# =========================
# TARGET ACCOUNT
# =========================

TARGET_USER = "target.gv"

# MESSAGE
MESSAGE = "Hello from Python Automation 🚀"

# =========================
# OPEN CHROME
# =========================

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()

wait = WebDriverWait(driver, 30)

# =========================
# OPEN INSTAGRAM
# =========================

driver.get("https://www.instagram.com/")

print("Instagram opened ✅")

# =========================
# LOGIN MANUALLY
# =========================

input("Login manually and then press Enter here...")

# =========================
# OPEN TARGET PROFILE
# =========================

driver.get(f"https://www.instagram.com/{TARGET_USER}/")

print("Target profile opened ✅")

time.sleep(10)
try:

    # =========================
    # FIND ALL BUTTONS
    # =========================

    buttons = driver.find_elements(By.TAG_NAME, "button")

    for button in buttons:

        if button.text == "Message":

            button.click()

            print("Message button clicked ✅")

            break

    time.sleep(8)

    # =========================
    # FIND MESSAGE BOX
    # =========================

    textbox = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[@role='textbox']"
            )
        )
    )

    # =========================
    # TYPE MESSAGE
    # =========================

    textbox.send_keys(MESSAGE)

    time.sleep(2)

    # =========================
    # SEND MESSAGE
    # =========================

    textbox.send_keys(Keys.RETURN)

    print("Message sent successfully ✅")

except Exception as e:

    print("Error occurred ❌")

    print(e)

input("Press Enter to close browser...")