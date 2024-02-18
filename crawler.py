from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import psycopg2
import time
from datetime import datetime
import pandas as pd

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

driver.close()

for div in range(len(information_array)):
    information_array[div] = information_array[div].split('|')
    for sub_index in range(len(information_array[div])):
        information_array[div][sub_index] = information_array[div][sub_index].strip()
        information_array[div][sub_index] = information_array[div][sub_index].replace('\n', " ")
        information_array[div][sub_index] = information_array[div][sub_index].replace('Date and Venue ', "")
        information_array[div][sub_index] = information_array[div][sub_index].split("Program")[0].strip()
        information_array[div][sub_index] = information_array[div][sub_index].split("Summer")[0].strip()

#-----------------------------------DATE, TIME, LOCATION-----------------------------------------------------
current_year = datetime.now().year

date_list = []
for sub_list in range(len(information_array)):
    date_string = information_array[sub_list][0]
    date = datetime.strptime(date_string, "%a %d.%m.")
    date = date.replace(year=current_year)
    date = date.strftime("%d-%m-%Y")
    date_list.append(date)

time_list = []
for sub_time in range(len(information_array)):
    time_string = information_array[sub_time][1]
    time_format = datetime.strptime(time_string, "%H.%M")
    time_format = time_format.strftime("%H:%M")
    time_list.append(time_format)

locations_list = []
for loc_index in range(len(information_array)):
    event_location = information_array[loc_index][2]
    if "Nr. 24" in event_location:
        event_location = information_array[loc_index][3]
        locations_list.append(event_location)
    else:
        locations_list.append(event_location)
#-----------------------CREATE DATAFRAME OBJECTS FOR EVENT, LOCATION, PERFORMERS------------------
location_df = pd.DataFrame(
    {
        "event_location": locations_list
    }
)
#--------------------------------Event Dataframe----------------------------------------------
event_date = []
event_time = []
event_title = []
event_image = []
event_performer = []
event_location = []

for index, title in enumerate(title_artist_array):
    performers = title.split("|")
    # print(performers)
    performers = [performer.strip() for performer in performers]
    # print(performers)

    #Get_date for each other list:
    date = date_list[index]
    time_instance = time_list[index]
    location = locations_list[index]
    image_url = image_link_array[index]


    # print(f"Title Matching Index Count: {index}")
    #Time to append
    for performer in performers:
        event_date.append(date)
        event_time.append(time_instance)
        event_location.append(location)
        event_image.append(image_url)
        event_performer.append(performer)
        event_title.append(title)

#Establish Event Dataframe
event_df = pd.DataFrame(
    {
        "event_date": event_date,
        "event_time": event_time,
        "event_title": event_title,
        "event_location": event_location,
        "event_performer": event_performer,
        "event_image": event_image
    }
)

names_works_df = pd.read_csv(r"C:\Users\Izrum\Desktop\nandw.csv")
#-----------------------------READY DATAFRAME OBJECTS FOR POSTGRES PARSING----------------
location_df = location_df.drop_duplicates(subset="event_location", keep="first")
location_df.insert(0, "location_id", range(1, 1+len(location_df)))
location_df.reset_index(drop=True, inplace=True)

event_df.insert(0, "event_id", range(10000, 10000+len(event_df)))
event_df = event_df.merge(location_df, on="event_location", how="left")
event_df = event_df.drop("event_location", axis=1)
# event_df.to_csv(r"C:\Users\Izrum\Desktop\events.csv")
# event_df = event_df.merge(names_works_df["performer_id"], on="event_performer", how="left")!!!!!!!!IMPORTANT


names_works_df = names_works_df.drop_duplicates(subset = "name", keep="first")
names_works_df = names_works_df.rename(columns={"Unnamed: 0" : "performer_id"})
names_works_df = names_works_df.rename(columns={"name" : "event_performer"})
names_works_df["performer_id"] = range(100, 100 + len(names_works_df))
names_works_df.reset_index(drop=True, inplace=True)
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
            id SERIAL NOT NULL,
            name VARCHAR(256) NOT NULL PRIMARY KEY,
            works TEXT
        )
        """,
        """
        CREATE TABLE event (
            id SERIAL PRIMARY KEY,
            event_date TEXT NOT NULL,
            event_time TEXT NOT NULL,
            event_title VARCHAR(256) NOT NULL,
            event_performer VARCHAR(256),
            event_image TEXT NOT NULL,
            event_location_id INTEGER NOT NULL            
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
def location_data():
    for index in range(0, len(location_df)):
        values = (int(location_df["location_id"][index]), location_df["event_location"][index])
        print(f"starting index with value: {index}")
        cursor.execute("INSERT INTO location (id, location_name) VALUES (%s, %s)", values)
        print(f"success, Let's Keep on Going!")
        time.sleep(2)

    print("Location Records updated!")
    conn.commit()

#MOVING NAME WORKS DATAFRAME TO PERFORMER TABLE IN POSTGRES
def works_data():
    for index in range(0, len(names_works_df)):
        values = (int(names_works_df["performer_id"][index]), names_works_df["event_performer"][index], names_works_df["works"][index])
        print(f"starting index with value: {index}")
        cursor.execute("INSERT INTO performer (id, name, works) VALUES (%s, %s, %s)", values)
        print(f"success, Let's Keep on Going!")
        time.sleep(2)

    conn.commit()
    print("Performer Records updated!")

#Moving Events DATAFRAME to EVENT TABLE IN POSTGRES
def event_data():
    for index in range(0, len(event_df)):
        values = (
            int(event_df["event_id"][index]),
            event_df["event_date"][index],
            event_df["event_time"][index],
            event_df["event_title"][index],
            event_df["event_performer"][index],
            event_df["event_image"][index],
            event_df["location_id"][index]
        )
        print(f"starting index with value: {index}")
        cursor.execute("""INSERT INTO event (id, event_date, event_time, event_title,
                        event_performer, event_image, event_location_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""", values)
        print(f"success, Let's Keep on Going!")
        time.sleep(2)

    conn.commit()
    print("event records updated")
#--------------------------------COMMAND EXECUTION FOR POSTGRES-----------------------------------
conn = establish_connection()
cursor = conn.cursor()
tables_creation()
#time.sleep(2)
# location_data()
#time.sleep(2)
# works_data()
#time.sleep(2)
# event_data()

