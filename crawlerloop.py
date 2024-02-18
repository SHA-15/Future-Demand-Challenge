from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pandas as pd
from datetime import datetime

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

# Now to Traverse towards Each page
time.sleep(1) #FROM 2
events_list = driver.find_elements(By.XPATH, "/html/body/div[4]/main/section/ul/li")

name_and_works_array = []
for event_entry in range(1, len(events_list)+1):
    #Go to the specified Event
    print(f"Starting the iteration with {event_entry}")
    events_page = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[4]/main/section/ul/li[{event_entry}]/div/div/div[2]/p/a")))
    #FROM 3
    print(f"/html/body/div[4]/main/section/ul/li[{event_entry}]/div/div/div[2]/p/a")

    #Take a Breather
    #time.sleep(1)#Changed from 2

    driver.execute_script("arguments[0].scrollIntoView();", events_page)
    driver.execute_script("arguments[0].click();", events_page)

    #Get the List of Elements in the Performers
    performers_list = driver.find_elements(By.XPATH, "/html/body/div[4]/main/section[1]/div[1]/div/div[1]/div/ul/li")

    #Traverse the list of performers
    #print(len(performers_list))
    for performer in range(1, len(performers_list) + 1):
        #Go through the performers page
        try:
            print("Trying the loop with the given condition")
            performer_page = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[4]/main/section[1]/div[1]/div/div[1]/div/ul/li[{performer}]/strong/a")))
            #Changed from 3
            print(f"Gotten the page with performer value {performer}")
            #print(f"/html/body/div[4]/main/section[1]/div[1]/div/div[1]/div/ul/li[{performer}]/strong")
            #Take a Breather
            #time.sleep(1) #Changed from 5

            #Move to Page
            #print("Trying to click")
            driver.execute_script("arguments[0].scrollIntoView();", performer_page)
            driver.execute_script("arguments[0].click();", performer_page)
            #Time to Extract Name and Tasks
            #print("I have moved to the performer page")

            #Take a Breather
            time.sleep(1) #Changed from 5

            name = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/header/div/div/div/div/div/div/h1")))
            #Change from 3
            works = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/section/div/div/div/div/p")))
            #Changed from 3
            #Create dictionary to extract tasks
            name_works_dict = {"event_performer": name.text, "works": works.get_attribute("innerText")}
            #print(name_works_dict)

            #Add the dict to the array
            name_and_works_array.append(name_works_dict)
            #print(name_and_works_array)

            #Return Back to the performers page for next performer_data
            driver.execute_script("window.history.go(-1)")
            time.sleep(1)
            # Changed from 4
            #print("I have returned back!")
            #WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[4]/main/section/ul/li[{event_entry}]/div/div/div[2]/p/a")))

        #To Deal with entries that do not contain the works data and to continue to loop,ensuring no pre_entries can be made
        except:
            #Create the dictionary to enter names and works to null
            null_name = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[4]/main/section[1]/div[1]/div/div[1]/div/ul/li[{performer}]/strong")))
            null_name_works_dict = {"event_performer": null_name.text, "works": "null"}

            #Append to array
            name_and_works_array.append(null_name_works_dict)

            #print(null_name_works_dict)
            continue

    #Now we need to traverse back to the event page to start the second iteration of the events
    driver.execute_script("window.history.go(-1)")
    time.sleep(2) #From 5
    #print(f"Starting the iteration after event_entry {event_entry}")

#print(name_and_works_array)

driver.close()

names_and_works_df = pd.DataFrame(name_and_works_array)

# print(names_and_works_df)
names_and_works_df.to_csv(r"C:\Users\Izrum\Desktop\nandw.csv")







