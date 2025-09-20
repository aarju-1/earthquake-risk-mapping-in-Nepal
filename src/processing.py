from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

website = 'https://seismonepal.gov.np/earthquakes'
path = "D:\chromedriver-win32\chromedriver-win32\chromedriver.exe"
service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(website)

rows = driver.find_elements(By.XPATH, "//tr[@data-key]")

# Print text of each row
for row in rows:
    print(row.text)

driver.quit()
