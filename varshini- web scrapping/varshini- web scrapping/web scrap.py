from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import os

driver = webdriver.Chrome()

driver.get("https://books.toscrape.com/")

all_books = []

for i in range(5):
    
    time.sleep(3)

    books = driver.find_elements(By.CLASS_NAME, "product_pod")

    for b in books:
        title = b.find_element(By.TAG_NAME, "h3").text
        price = b.find_element(By.CLASS_NAME, "price_color").text
        rating = b.find_element(By.CLASS_NAME, "star-rating").get_attribute("class").split()[-1]

        # clean price
        price = price.replace("£", "")

        # convert rating
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        rating = rating_map.get(rating, rating)

        all_books.append([title, price, rating])

    # next page click
    try:
        next_btn = driver.find_element(By.LINK_TEXT, "next")
        next_btn.click()
    except:
        break
print("total books:",len(all_books))
print("current folder:",os.getcwd())
with open("books_data.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Rating"])
    writer.writerows(all_books)

print("Data saved to books_data.csv")

input("Press Enter to close...")