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
from datetime import datetime

import pandas as pd
import numpy as np

#Set Dataframe visibility
pd.set_option("display.max_colwidth", None)

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
#TITLE & ARTIST
title_artist_array = []
#Image Links
image_link_array = []
i = 1
while i >= 1:
    try:
        information_array.append(driver.find_element(By.XPATH, f'html/body/div[4]/main/section/ul/li[{i}]/div/div/div[2]/div[2]').text)
        title_artist_array.append(driver.find_element(By.XPATH, f'/html/body/div[4]/main/section/ul/li[{i}]/div/div/div[2]/p/a').text)
        image_link_array.append("https://www.lucernefestival.ch" + driver.find_element(By.XPATH, f'/html/body/div[4]/main/section/ul/li[{i}]/div/div/div[1]/a/figure/picture/source[1]').get_attribute('srcset'))
        # print(data_point)
        i += 1
    except:
        print("Function cycle ended at: %d, no more entries found" %i)
        break


for div in range(len(information_array)):
    information_array[div] = information_array[div].split('|')
    for sub_index in range(len(information_array[div])):
        information_array[div][sub_index] = information_array[div][sub_index].strip()
        information_array[div][sub_index] = information_array[div][sub_index].replace('\n', " ")
        information_array[div][sub_index] = information_array[div][sub_index].replace('Date and Venue ', "")
        information_array[div][sub_index] = information_array[div][sub_index].split("Program")[0].strip()
        information_array[div][sub_index] = information_array[div][sub_index].split("Summer")[0].strip()

#-----------------------------------DATE, TIME, LOCATION-----------------------------------------------------
#Get Dates
current_year = datetime.now().year

date_list = []
for sub_list in range(len(information_array)):
    date_string = information_array[sub_list][0]
    date = datetime.strptime(date_string, "%a %d.%m.")
    date = date.replace(year=current_year)
    date = date.strftime("%d-%m-%Y")
    date_list.append(date)

#Get Time
time_list = []
for sub_time in range(len(information_array)):
    time_string = information_array[sub_time][1]
    time_format = datetime.strptime(time_string, "%H.%M")
    time_format = time_format.strftime("%H:%M")
    time_list.append(time_format)


#Get Locations
locations_list = []
for loc_index in range(len(information_array)):
    event_location = information_array[loc_index][2]
    if "Nr. 24" in event_location:
        event_location = information_array[loc_index][3]
        locations_list.append(event_location)
    else:
        locations_list.append(event_location)


#Creating a DataFrame Object
event_information_df = pd.DataFrame(
    {
        "Date": date_list,
        "Time": time_list,
        "Location": locations_list
    }
)


print(event_information_df)
#--------------------------------Event Title----------------------------------------------
title_df = pd.DataFrame(
    {
        "Title": title_artist_array
    }
)

print(title_df)

#--------------------------------Image Links-----------------------------------------------
image_df = pd.DataFrame(
    {
    "Image_URL": image_link_array
    }
)

print(image_df)