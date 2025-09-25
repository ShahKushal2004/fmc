import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # keep browser open
driver = webdriver.Chrome(options=options)

# Open the website
driver.get("https://www.jiomart.com/")  
driver.maximize_window()

print("👉 Please manually set the location to Malad 400097")
input("✅ Press ENTER here once location is set...")

product_data = []  # List to hold product info

def add_to_cart(product_name):
    try:
        # Search for the product
        search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Search']")
        search_box.clear()
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        wait = WebDriverWait(driver, 10)

        # Wait for product cards to load
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'product')]")))

        # Get first product card
        product_card = driver.find_element(By.XPATH, "//div[contains(@class, 'product')]")

        # Get product title
        try:
            title = product_card.find_element(By.XPATH, ".//div[contains(@class, 'name')]").text.strip()
        except:
            title = product_name  # fallback if name not found

        # Get product price
        try:
            price = product_card.find_element(By.XPATH, ".//span[contains(@class, 'price')]").text.strip()
        except:
            price = "N/A"

        # Try to add to cart (Method 1)
        try:
            add_button = product_card.find_element(By.XPATH, ".//button[contains(., 'Add')]")
            add_button.click()
            print(f"✅ Added {title} @ {price}")
        except:
            print(f"⚠️ Could not click Add for {title}")

        # Save product info
        product_data.append({"Product": title, "Price": price})

    except Exception as e:
        print(f"❌ Error for {product_name}: {e}")

# ---- MAIN ----
products = ["Onion", "Tomato"]

for p in products:
    add_to_cart(p)
    time.sleep(2)

# Save to CSV
csv_file = "products.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Product", "Price"])
    writer.writeheader()
    writer.writerows(product_data)

print(f"📦 Data saved to {csv_file}")
print("🎯 Process Completed")
