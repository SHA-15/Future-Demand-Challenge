# Future Demand Challenge

![image](https://github.com/SHA-15/Future-Demand-Challenge/assets/148129383/b71dd518-57db-48d5-9455-43817a0d8cb7)

The Tasks implements a Web Crawler and Scraper program in Python using the Selenium 🚀 Library to be able to parse our website's data into the POSTGRESQL DATABASE ⏺️. The following are the libraries utilized for the execution of the project:
1. Selenium 🔩
2. Pandas ⚡
3. psycopg2 📰
4. datetime & time ⏲️

Reason for choosing Selenium over other frameworks:
👍 Selenium excels in dealing with core javascript based web applications, but it's good for projects where speed isn't relevant.
👍 Beautiful Soap provides greater access in parsing static HTML elements, but does not cater well towards JAVASCRIPT Features.
👍 Selenium allows integration of JS triggers and shares similarities with DOM object interactivities such as clicking.

The Program Structure:

The entire program is broken down into 3 Distinct Elements:
1. Two-Part Data Access Process
2. Data Manipulation and Cleansing (Utilizing Pandas)
3. Data Load to PostgreSQL

![image](https://github.com/SHA-15/Future-Demand-Challenge/assets/148129383/bcaab539-f51c-49b6-9246-5683cf5abc6c)

-The Class "Webcrawler()" instantiates the webdriver and options properties as well as housing the methods to traverse the front page and the performer pages.

🔍Access_parsing_elements() is focused towards the 'Summer Festival 2024' It traverses each <li></li> tag and accesses the text elements to attain "TITLE", "DATE", "TIME", "IMAGE" and "LOCATION" attributes for our data cleansing.
🔍Access_performer_works() visits each page to identify each performer and further visits the performers to acquire their summaries. Here we utilize .execute_scripts() for JS scroll and clicking functionality, Implicit and Explicit Waits for server response readiness. 

🔣 Other methods defined within the class are primarily focused on DATAFRAME Operations. The focus was to enture minimized data cluttering and erroneous values within PostgreSQL to be populated. Data segregation was performed across 3 areas:
🥇 Events
🥈 Performers
🥉 Locations

This provided greater clarity in data visibility and realtionships for our DATABASE Schema

![image](https://github.com/SHA-15/Future-Demand-Challenge/assets/148129383/954f7d87-fd9a-4d85-a94a-d34c5eb60e54)

ℹ️ FOLLOWING IS THE DATABASE SCHEMA EMPLOYED FOR PostgreSQL

![image](https://github.com/SHA-15/Future-Demand-Challenge/assets/148129383/850331ba-3518-4a8f-b828-854cea20c0b0)




