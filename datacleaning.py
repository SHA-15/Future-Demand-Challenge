import numpy as np
import pandas as pd
from datetime import datetime

x = [['Tue 13.08.', '19.30', 'KKL Luzern, Concert Hall', 'Elgar', 'Ljatoschynskyj', 'Respighi', '12 pm (CET) starting at CHF 50'], ['Wed 14.08.', '19.30', 'KKL Luzern, Concert Hall', 'Britten', 'Strauss', '12 pm (CET) starting at CHF 50'], ['Fri 16.08.', '18.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Sat 17.08.', '18.30', 'KKL Luzern, Concert Hall', 'Grieg', 'Schumann', '12 pm (CET) starting at CHF 40'], ['Sun 18.08.', '11.00', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Sun 18.08.', '15.30', 'KKL Luzern, Lucerne Hall', 'Rihm', 'Furrer', 'Streich', '12 pm (CET) starting at CHF 50'], ['Sun 18.08.', '19.30', 'KKL Luzern, Concert Hall', 'Schoenberg', '12 pm (CET) starting at CHF 30'], ['Mon 19.08.', '19.30', 'KKL Luzern, Concert Hall', 'de Séverac', 'Chopin', 'Prokofiev', 'Schumann', '12 pm (CET) starting at CHF 30'], ['Tue 20.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Wed 21.08.', '17.00', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Thu 22.08.', '12.15', 'Lukaskirche', '12 pm (CET) starting at CHF 30'], ['Thu 22.08.', '19.30', 'KKL Luzern, Concert Hall', 'Schubert', '12 pm (CET) starting at CHF 30'], ['Fri 23.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Sat 24.08.', '11.00', 'KKL Luzern, Lucerne Hall', 'Streich', 'Rihm', 'Boulez', '12 pm (CET) starting at CHF 50'], ['Sat 24.08.', '18.30', 'KKL Luzern, Concert Hall', 'Bruckner', '12 pm (CET) starting at CHF 40'], ['Sat 24.08.', '21.30', 'Luzerner Theater, Theatersaal', 'Gnattali', 'Brouwer', 'Marino Arcaro', 'Piazzolla', '12 pm (CET) starting at CHF 50'], ['Sun 25.08.', '14.30', 'KKL Luzern, Lucerne Hall', '12 pm (CET) starting at CHF 50'], ['Sun 25.08.', '18.30', 'KKL Luzern, Concert Hall', 'Mozart', 'Debussy', 'Ravel', '12 pm (CET) starting at CHF 30'], ['Mon 26.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Tue 27.08.', '12.15', 'Lukaskirche', '12 pm (CET) starting at CHF 30'], ['Tue 27.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Wed 28.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Thu 29.08.', '12.15', 'Lukaskirche', 'Strauss', 'Kirchner', 'Vignery', '12 pm (CET) starting at CHF 30'], ['Thu 29.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Fri 30.08.', '19.30', 'KKL Luzern, Concert Hall', 'Beethoven', 'Fauré', 'Ravel', '12 pm (CET) starting at CHF 40'], ['Sat 31.08.', '11.00', 'KKL Luzern, Lucerne Hall', '12 pm (CET) starting at CHF 50'], ['Sat 31.08.', '16.00', 'Lukaskirche, Kirchensaal', '12 pm (CET) starting at CHF 50'], ['Sat 31.08.', '19.30', 'KKL Luzern, Concert Hall', 'Streich', 'Feldman', '12 pm (CET) starting at CHF 30'], ['Sun 01.09.', '11.00', 'KKL Luzern, Concert Hall', 'Widmann', 'Schumann', '12 pm (CET) starting at CHF 30'], ['Sun 01.09.', '16.00', 'Luzerner Theater, Theatersaal', '12 pm (CET) starting at CHF 50'], ['Sun 01.09.', '18.30', 'KKL Luzern, Concert Hall', 'Tchaikovsky', '12 pm (CET) starting at CHF 40'], ['Mon 02.09.', '19.30', 'Nr. 241323', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Tue 03.09.', '12.15', 'Lukaskirche', 'Debussy', 'Holliger', 'Elgar', 'Schnyder', '12 pm (CET) starting at CHF 30'], ['Tue 03.09.', '19.30', 'KKL Luzern, Concert Hall', 'Marsalis', 'Price', '12 pm (CET) starting at CHF 30'], ['Wed 04.09.', '19.30', 'KKL Luzern, Concert Hall', 'Bruckner', '12 pm (CET) starting at CHF 40'], ['Thu 05.09.', '12.15', 'Lukaskirche', 'Schumann', 'Mendelssohn', 'Nielsen', 'Gubaidulina', '12 pm (CET) starting at CHF 30'], ['Thu 05.09.', '19.30', 'KKL Luzern, Concert Hall', 'Berlioz', '12 pm (CET) starting at CHF 40'], ['Fri 06.09.', '19.30', 'KKL Luzern, Concert Hall', 'Strauss', '12 pm (CET) starting at CHF 40'], ['Sat 07.09.', '11.00', 'Hochschule Luzern – Music, Salquin Concert Hall', 'Streich', '12 pm (CET) starting at CHF 50'], ['Sat 07.09.', '14.30', 'KKL Luzern, Concert Hall', 'Norman', 'Abrahamsen', '12 pm (CET) starting at CHF 30'], ['Sat 07.09.', '19.30', 'Nr. 241328', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Sun 08.09.', '11.00', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Sun 08.09.', '16.00', 'Hochschule Luzern – Music, Salquin Concert Hall', '12 pm (CET) starting at CHF 50'], ['Sun 08.09.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Mon 09.09.', '19.30', 'KKL Luzern, Concert Hall', 'Dvořák', '12 pm (CET) starting at CHF 30'], ['Tue 10.09.', '12.15', 'Lukaskirche', '12 pm (CET) starting at CHF 30'], ['Tue 10.09.', '19.30', 'KKL Luzern, Concert Hall', 'Beethoven', 'Chopin', '12 pm (CET) starting at CHF 30'], ['Wed 11.09.', '19.30', 'KKL Luzern, Concert Hall', 'Mahler', '12 pm (CET) starting at CHF 30'], ['Thu 12.09.', '12.15', 'Lukaskirche', 'Liszt', 'Zhao', 'Gershwin', '12 pm (CET) starting at CHF 30'], ['Thu 12.09.', '19.30', 'KKL Luzern, Concert Hall', 'Dutilleux', 'Seltenreich', 'Ben-Haim', '12 pm (CET) starting at CHF 30'], ['Fri 13.09.', '19.30', 'KKL Luzern, Concert Hall', 'Bruckner', '12 pm (CET) starting at CHF 40'], ['Sat 14.09.', '18.30', 'KKL Luzern, Concert Hall', 'Bartók', 'Dvořák', '12 pm (CET) starting at CHF 30'], ['Sun 15.09.', '18.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30']]






#Get Dates
current_year = datetime.now().year

date_list = []
for sub_list in range(len(x)):
    date_string = x[sub_list][0]
    date = datetime.strptime(date_string, "%a %d.%m.")
    date = date.replace(year=current_year)
    date = date.strftime("%d-%m-%Y")
    date_list.append(date)

#Get Time
time_list = []
for sub_time in range(len(x)):
    time_string = x[sub_time][1]
    time_format = datetime.strptime(time_string, "%H.%M")
    time_format = time_format.strftime("%H:%M")
    time_list.append(time_format)


#Get Locations
locations_list = []
for loc_index in range(len(x)):
    event_location = x[loc_index][2]
    if "Nr. 24" in event_location:
        event_location = x[loc_index][3]
        locations_list.append(event_location)
    else:
        locations_list.append(event_location)


#Creating a DataFrame Object
df = pd.DataFrame(
    {
        "Date" : date_list,
        "Time": time_list,
        "Location": locations_list
    }
)



print(df)

