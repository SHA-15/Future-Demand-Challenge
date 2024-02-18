# SELENIUM WEBDRIVER ELEMENTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# DATA PROCESSING ELEMENTS
import psycopg2
import time
from datetime import datetime
import pandas as pd

# Set Dataframe Visibility
pd.set_option("display.max_colwidth", None)


class Webcrawler:
    def __init__(self):
        # Set Chrome options
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.service = Service(r".\chromedriver\chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.information_array = []
        self.title_artist_array = []
        self.image_link_array = []
        self.name_and_works_array = []
        self.location_df = {}
        self.event_df = {}


    def navigate_url(self, url="https://www.lucernefestival.ch/en/program/summer-festival-24"):
        #Initialize the Chrome Driver

        self.driver.get(url)

        # Maximize Browser Window
        self.driver.maximize_window()

        # Allow loading of all elements
        time.sleep(1) #From 2

        cookies = self.driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/div[3]/aside/button[1]")
        cookies.click()

        print(f"Page title is: {self.driver.title}")

    def access_parsing_elements(self):
        # time.sleep(1)

        # Identify Entries for Traversal
        events_list = self.driver.find_elements(By.XPATH, "/html/body/div[4]/main/section/ul/li")

        for element_data in range(1, len(events_list)+1):
            self.information_array.append(self.driver.find_element(By.XPATH, f'html/body/div[4]/main/section/ul/li[{element_data}]/div/div/div[2]/div[2]').text)
            self.title_artist_array.append(self.driver.find_element(By.XPATH, f"/html/body/div[4]/main/section/ul/li[{element_data}]/div/div/div[2]/p/a").text)
            self.image_link_array.append("https://www.lucernefestival.ch" + self.driver.find_element(By.XPATH, f"/html/body/div[4]/main/section/ul/li[{element_data}]/div/div/div[1]/a/figure/picture/source[1]").get_attribute('srcset'))
            print(f"Information, title, artists, images captured of event #{element_data}")

        print("Primary Data extraction from first page concluded")

        self.driver.close()

    # Segregate Date, Time and Location within information array
    def retrieve_location(self):
        for inf in range(len(self.information_array)):
            print(f"Starting the separation of location from other text, at position {inf}")
            self.information_array[inf] = self.information_array[inf].split("|")
            for index in range(len(self.information_array[inf])):
                self.information_array[inf][index] = self.information_array[inf][index].strip()
                self.information_array[inf][index] = self.information_array[inf][index].replace("\n", " " )
                self.information_array[inf][index] = self.information_array[inf][index].replace("Date and Venue ", "")
                self.information_array[inf][index] = self.information_array[inf][index].split("Program")[0].strip()
                self.information_array[inf][index] = self.information_array[inf][index].split("Summer")[0].strip()

            print(f"Completed extraction at position, {inf} with {self.information_array[inf][2]}")

        print("Execution completed")
    # Attain clean list for dataframe creation
    def date_time_location(self):
        current_year = datetime.now().year
        date_list = []
        time_list = []
        locations_list = []

        for sub in range(len(self.information_array)):
            #Date List
            date_string = self.information_array[sub][0]
            date = datetime.strptime(date_string, "%a %d.%m.")
            date = date.replace(year=current_year)
            date = date.strftime("%d-%m-%Y")
            date_list.append(date)
            #Time List
            time_string = self.information_array[sub][1]
            time_format = datetime.strptime(time_string, "%H.%M")
            time_format = time_format.strftime("%H:%M")
            time_list.append(time_format)
            #Locations List
            event_location = self.information_array[sub][2]
            if "Nr. 24" in event_location:
                event_location = self.information_array[sub][3]
                locations_list.append(event_location)
            else:
                locations_list.append(event_location)

        return date_list, time_list, locations_list

    def create_df(self):
        # Attain the results of the list extraction
        date_list, time_list, locations_list = self.date_time_location()

        # Location Dataframe
        self.location_df = pd.DataFrame(
            {
                "event_location": locations_list
            }
        )

        # Event Dataframe
        event_date = []
        event_time = []
        event_title = []
        event_image = []
        event_performer = []
        event_location = []

        for index, title in enumerate(self.title_artist_array):
            performers = title.split("|")

            performers = [performer.strip() for performer in performers]

            #Get data for each parameter from the original list
            date = date_list[index]
            time_instance = time_list[index]
            location = locations_list[index]
            image_url = self.image_link_array[index]

            print(f"We iterate over {performers}: Array iteration {index}")
            for performer in performers:
                event_date.append(date)
                event_time.append(time_instance)
                event_location.append(location)
                event_image.append(image_url)
                event_performer.append(performer)
                event_title.append(title)

            print(f"{event_title[-1]} has been added to the dataframe primer")

        self.event_df = pd.DataFrame(
            {
                "event_date": event_date,
                "event_time": event_time,
                "event_title": event_title,
                "event_location": event_location,
                "event_performer": event_performer,
                "event_image": event_image
            }
        )

    # def access_name_works(self):


# lucerne_crawler = Webcrawler()
# lucerne_crawler.navigate_url()
# lucerne_crawler.access_parsing_elements()
# lucerne_crawler.retrieve_location()
# lucerne_crawler.date_time_location()
# lucerne_crawler.create_df()



