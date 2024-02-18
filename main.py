# SELENIUM WEBDRIVER ELEMENTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver_py import binary_path
from webdriver_manager.chrome import ChromeDriverManager

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
        self.options.add_argument("--headless")  # Make Chrome run headlessly
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_experimental_option("detach", True)
        #self.service = webdriver.ChromeService(binary_path=binary_path)
        self.driver = webdriver.Chrome(service=Service( ChromeDriverManager().install()),options=self.options)
        self.information_array = []
        self.title_array = []
        self.image_link_array = []
        self.performers_array = []
        self.performer_and_works_array = []
        self.location_df = {}
        self.event_df = {}
        self.performer_works_df = {}

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
            self.title_array.append(self.driver.find_element(By.XPATH, f"/html/body/div[4]/main/section/ul/li[{element_data}]/div/div/div[2]/p/a").text)
            self.image_link_array.append("https://www.lucernefestival.ch" + self.driver.find_element(By.XPATH, f"/html/body/div[4]/main/section/ul/li[{element_data}]/div/div/div[1]/a/figure/picture/source[1]").get_attribute('srcset'))
            print(f"Information, title, images captured of event #{element_data}")

        print("Primary Data extraction from first page concluded")

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
        self.retrieve_location()
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

        for index, title in enumerate(self.title_array):

            #Get data for each parameter from the original list
            date = date_list[index]
            time_instance = time_list[index]
            location = locations_list[index]
            image_url = self.image_link_array[index]

            print(f"We iterate over performers: Array iteration {index}")
            for performer in self.performers_array[index]:
                print(f"Performer: {performer}")
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

    def access_performer_works(self):
        #Primary Looping mechanism
        events_list = self.driver.find_elements(By.XPATH, "/html/body/div[4]/main/section/ul/li")

        for event in range(1, len(events_list) + 1):

            print(f"Start from event page, look at event: {event}")
            events_page = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[4]/main/section/ul/li[{event}]/div/div/div[2]/p/a")))

            #Execute Click via JS
            self.driver.execute_script("arguments[0].scrollIntoView();", events_page)
            self.driver.execute_script("arguments[0].click();", events_page)

            print("Entered the events webpage")

            # Get list of elements in Performers
            performers_list = self.driver.find_elements(By.XPATH, "/html/body/div[4]/main/section[1]/div[1]/div/div[1]/div/ul/li")

            # Traverse the list of performers
            print(f"Initiating Iteration of {len(performers_list)} Performers in Events Page.")
            performers_sublist = []
            for performer in range(1, len(performers_list) + 1):
                # BEFORE GRABBING ELEMENTS, IT GRABS THE NAME AND APPENDS TO THE PERFORMER LIST
                performer_name = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[4]/main/section[1]/div[1]/div/div[1]/div/ul/li[{performer}]/strong"))).text
                performers_sublist.append(performer_name)
                print(f"{performer_name} has been append to the performers_array")

                try:
                    print(f"Iteration check performer {performer}")
                    performer_page = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[4]/main/section[1]/div[1]/div/div[1]/div/ul/li[{performer}]/strong/a")))

                    # Move Towards Page
                    self.driver.execute_script("arguments[0].scrollIntoView();", performer_page)
                    self.driver.execute_script("arguments[0].click();", performer_page)
                    print("Successfully Entered into Performer page")

                    #Take a Breather
                    time.sleep(1) # Changed from 5

                    #Wait time reduced from 3 for both variables
                    works = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/section/div/div/div/div/p")))

                    #Initialize dictionary to create dict_list
                    performer_works_dict = {"event_performer": performer_name, "works": works.get_attribute("innerText")}

                    print(f"Artist for the event: {performer_works_dict['event_performer']}")

                    self.performer_and_works_array.append(performer_works_dict)

                    #Return to main event page
                    self.driver.execute_script("window.history.go(-1)")
                    time.sleep(1) # Changed from 4


                #Deal with performers with null values
                except:
                    print(f"performer {performer_name} in event page {event} is null")

                    null_name_works_dict = {"event_performer": performer_name, "works": "null"}
                    print(f"{null_name_works_dict['event_performer']} provided no sequential data")

                    #Append
                    self.performer_and_works_array.append(null_name_works_dict)


            self.performers_array.append(performers_sublist)
            print(self.performers_array[-1])

            #Traverse back to events page after inner loop completes
            self.driver.execute_script("window.history.go(-1)")
            time.sleep(1) # Change from 5 and 2!!

    def convert_performer_works_df(self):
        self.access_performer_works()
        self.performer_works_df = pd.DataFrame(self.performer_and_works_array)

    def postgres_readiness(self):
        #Location Dataframe
        self.location_df = self.location_df.drop_duplicates(subset="event_location", keep="first")
        self.location_df.insert(0, "location_id", range(1, 1+len(self.location_df)))
        self.location_df.reset_index(drop=True, inplace=True)

        #Performers and Works Dataframe
        self.performer_works_df = self.performer_works_df.drop_duplicates(subset="event_performer", keep="first")
        self.performer_works_df.insert(0, "performer_id", range(1, 1+len(self.performer_works_df)))
        self.performer_works_df.reset_index(drop=True, inplace=True)

        # Event Dataframe
        self.event_df.insert(0, "event_id", range(10000, 10000 + len(self.event_df)))
        self.event_df = self.event_df.merge(self.location_df, on="event_location", how="left")
        self.event_df = self.event_df.drop("event_location", axis=1)
        performer_subset = self.performer_works_df[["performer_id", "event_performer"]]
        self.event_df = self.event_df.merge(performer_subset, on="event_performer", how="left")
        self.event_df = self.event_df.drop("event_performer", axis=1)


lucerne_crawler = Webcrawler()
lucerne_crawler.navigate_url()
lucerne_crawler.access_parsing_elements()
lucerne_crawler.convert_performer_works_df()
lucerne_crawler.create_df()
lucerne_crawler.driver.close()
lucerne_crawler.postgres_readiness()


#--------------------------------Build Connection To POSTGRES-----------------------------
def establish_connection(database_value="FutureDemand", user_value="postgres", password="abcd1234", host="localhost"):
    try:
        connection = psycopg2.connect(
            database=database_value,
            user=user_value,
            password=password,
            host=host
        )
        print("Database connection successful")

    except Exception as e:
        print(f"Table Creation Error: {e}")

    return connection

def tables_creation():
    # Creating Tables
    tables = (
        """
        CREATE TABLE location (
            id SERIAL PRIMARY KEY,
            location_name VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE performer (
            id SERIAL PRIMARY KEY,
            name VARCHAR(256) NOT NULL,
            works TEXT
        )
        """,
        """
        CREATE TABLE event (
            id SERIAL PRIMARY KEY,
            event_date TEXT NOT NULL,
            event_time TEXT NOT NULL,
            event_title VARCHAR(256) NOT NULL,
            event_image TEXT NOT NULL,
            location_id SERIAL REFERENCES location (id),
            performer_id SERIAL REFERENCES performer (id)          
        )
        """
    )

    try:
        for table in tables:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = %s
                )
                """, (table.split()[2],)
            )
            table_exists = cursor.fetchone()[0]
            if table_exists:
                print("Table already exists")
            else:
                cursor.execute(table)
                print("Table Creation Complete")
            #Allow Delay between Creations
            time.sleep(2)

        print("Tables created successfully")

    except Exception as e:
        print(f"Unable to create Tables: {e}")

    conn.commit()
#---------------------------MOVING DATA TO TABLES----------------------------------------
#MOVING LOCATION DATAFRAME TO LOCATION TABLE in POSTGRES
def location_data(object):
    for index in range(0, len(object.location_df)):
        values = (int(object.location_df["location_id"][index]), object.location_df["event_location"][index])
        print(f"starting location data input : {index}")
        cursor.execute("INSERT INTO location (id, location_name) VALUES (%s, %s)", values)
        print(f"Location input success!")
        time.sleep(2)

    print("Location Records updated!")
    conn.commit()

#MOVING NAME WORKS DATAFRAME TO PERFORMER TABLE IN POSTGRES
def performer_works_data(object):
    for index in range(0, len(object.performer_works_df)):
        values = (int(object.performer_works_df["performer_id"][index]), object.performer_works_df["event_performer"][index], object.performer_works_df["works"][index])
        print(f"starting performer data input: {index}")
        cursor.execute("INSERT INTO performer (id, name, works) VALUES (%s, %s, %s)", values)
        print(f"Performer input success!")
        time.sleep(2)

    conn.commit()
    print("Performer Records updated!")

#Moving Events DATAFRAME to EVENT TABLE IN POSTGRES
def event_data(object):
    for index in range(0, len(object.event_df)):
        values = (
            int(object.event_df["event_id"][index]),
            object.event_df["event_date"][index],
            object.event_df["event_time"][index],
            object.event_df["event_title"][index],
            object.event_df["event_image"][index],
            int(object.event_df["location_id"][index]),
            int(object.event_df["performer_id"][index])
        )
        print(f"Starting event data input: {index}")
        cursor.execute("""INSERT INTO event (id,event_date,event_time,event_title,event_image,location_id,performer_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""", values)
        print(f"Event input success!")
        time.sleep(2)

    conn.commit()
    print("event records updated")
# #--------------------------------COMMAND EXECUTION FOR POSTGRES-----------------------------------
conn = establish_connection()
cursor = conn.cursor()
tables_creation()
# time.sleep(2)
location_data(lucerne_crawler)
# time.sleep(2)
performer_works_data(lucerne_crawler)
# time.sleep(2)
event_data(lucerne_crawler)
