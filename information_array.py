from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

import pandas as pd
import numpy as np

# Set Chrome options
options = Options()
options.add_experimental_option("detach", True)

# Specify the full path to chromedriver.exe
chrome_driver_path = r"C:\Users\Izrum\Desktop\chromedriver.exe"

# Initialize Chrome WebDriver with Service object
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the specified URL
url = "https://www.lucernefestival.ch/en/program/summer-festival-24"
driver.get(url)

# Maximize the browser window
driver.maximize_window()

#Allow web site to load prior to execution of crawler
time.sleep(2)

#Accept Cookies on browser startup
cookies = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/div[3]/aside/button[1]")
cookies.click()

print(f"Page title is: {driver.title}")

#-------------------------ACCESSING NECESSARY ELEMENTS FOR DATA PARSING--------------------------

# DATE, TIME, LOCATION
information_array = []
i = 1
while i >= 1:
    try:

        information_array.append(driver.find_element(By.XPATH, f'html/body/div[4]/main/section/ul/li[{i}]/div/div/div[2]/div[2]').text)

        # print(data_point)
        i += 1

    except:
        # print("Function cycle ended at: %d, no more entries found" %i)
        break


for div in range(len(information_array)):
    information_array[div] = information_array[div].split('|')
    for sub_index in range(len(information_array[div])):
        information_array[div][sub_index] = information_array[div][sub_index].strip()
        information_array[div][sub_index] = information_array[div][sub_index].replace('\n', " ")
        information_array[div][sub_index] = information_array[div][sub_index].replace('Date and Venue ', "")
        information_array[div][sub_index] = information_array[div][sub_index].split("Program")[0].strip()
        information_array[div][sub_index] = information_array[div][sub_index].split("Summer")[0].strip()

print(information_array)

#TITLE & ARTIST
title_artist_array = []
t = 1
#Using the same iterator variable i
while t >= 1:
    try:

        title_artist_array.append(driver.find_element(By.XPATH, f'/html/body/div[4]/main/section/ul/li[{t}]/div/div/div[2]/p/a').text)

        # print(f"Array iteration: {x}")

        t += 1

    except:
        break

#IMAGE LINK
image_link_array = []
l = 1
while l >= 1:
    try:

        #Concatenating the HTTP address with the srcset attribute value to generate URL
        image_link_array.append("https://www.lucernefestival.ch" + driver.find_element(By.XPATH, f'/html/body/div[4]/main/section/ul/li[{l}]/div/div/div[1]/a/figure/picture/source[1]').get_attribute('srcset'))

        #print(f"Array iteration: {l}")

        l += 1
    except:
        break