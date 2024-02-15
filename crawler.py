from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.headless = True
options.add_experimental_option("detach", True)

svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc, options=options)

driver.get("https://www.lucernefestival.ch/en/program/summer-festival-24")
driver.maximize_window()

#Allow web site to load before executing crawl
time.sleep(2)

# Accept cookies on browser startup
cookies = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/div[3]/aside/button[1]")
#Click upon opening
cookies.click()

print(f"Page title is: {driver.title}")
