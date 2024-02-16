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

#-------------------------ACCESSING NECESSARY ELEMENTS FOR DATA PARSING--------------------------

# DATE, TIME, LOCATION
information_array = []
i = 1
while i >= 1:
    try:
        information_array.append(driver.find_element(By.XPATH, f'html/body/div[4]/main/section/ul/li[{i}]/div/div/div[2]/div[2]').text)
        # print(data_point)
        i+= 1
    except:
        # print("Function cycle ended at: %d, no more entries found" %i)
        break

for div in range(len(information_array)):
    information_array[div] = information_array[div].split('|')


# print(information_array[0], information_array[23])

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

# print(title_artist_array[0])


#IMAGE LINK
image_link_array = []
l = 1
while l >= 1:
    try:
        #Concatenating the HTTP address with the srcset attribute value to generate URL
        image_link_array.append("https://www.lucernefestival.ch" + driver.find_element(By.XPATH, f'/html/body/div[4]/main/section/ul/li[{l}]/div/div/div[1]/a/figure/picture/source[1]').get_attribute('srcset'))
        print(f"Array iteration: {l}")
        l += 1
    except:
        break


# image_source_test = driver.find_element(By.XPATH, '/html/body/div[4]/main/section/ul/li[1]/div/div/div[1]/a/figure/picture/source[1]').get_attribute('srcset')

# print(image_link_array[36])



