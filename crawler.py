# Import Selenium Library
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


information_array = []
i = 1
while i >= 1:
    try:
        data_point = [driver.find_element(By.XPATH, f'html/body/div[4]/main/section/ul/li[{i}]/div/div/div[2]/div[2]').text]
        information_array.append(data_point)
        # print(data_point)
        i+= 1
    except:
        # print("Function cycle ended at: %d, no more entries found" %i)
        break

print(information_array[0])


