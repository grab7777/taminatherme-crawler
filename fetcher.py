import re
import os
import psycopg2

# from requests_html import HTMLSession
# import urllib.request
# import mechanize
from dotenv import load_dotenv
from datetime import datetime
from pyppeteer import launch
import asyncio
# from selenium import webdriver

load_dotenv()
# TODO: installation of python-dotenv, psycopg2, selenium

async def loadSource():
    browser = await launch(headless=True,args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-software-rasterizer', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.goto("https://www.taminatherme.ch")
    html_content = await page.content()
    
    # session = HTMLSession()
    # response = session.get('https://www.taminatherme.ch')
    # response.html.render()
    # print(html_content)
    await page.close()
    await browser.close()
    # page = urllib.request.urlopen('https://www.taminatherme.ch')
    return html_content
    # chrome = webdriver.Chrome()
    # chrome.get("https://www.taminatherme.ch")

source = asyncio.run(loadSource())
def getOccupancy(sourceString):
    result = re.search(r"<span class=\"block font-bold\">([0-9]+)%</span>", sourceString)
    if result.group(1) and int(result.group(1)) >= 0 and int(result.group(1)) <= 100:
        print("Occupancy: " + result.group(1))
        return int(result.group(1))
    else:
        print("Could not find occupancy on Website")
        exit(0)

def writeNewValueIntoDataBase(timestamp, occupancy):
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_DATABASE_NAME = os.getenv("DB_DATABASE_NAME")
    connection = psycopg2.connect(database = DB_DATABASE_NAME, 
                        user = DB_USER, 
                        host= DB_HOST,
                        password = DB_PASSWORD,
                        port = DB_PORT)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS occupancy(
                timestamp timestamp PRIMARY KEY,
                occupancy integer NOT NULL,
                CONSTRAINT occ_valid CHECK (occupancy >= 0 AND occupancy <= 100));
                """)
    cursor.execute(f"INSERT INTO occupancy(timestamp, occupancy) VALUES({timestamp},{occupancy})");
    connection.commit()
    # TODO: Error handling

occupancy = getOccupancy(source)
logFile = open("/cron_task.log", "a")
# move this to the function, where we wrote the value into the database
logFile.write(f"Date: {datetime.now()}\t Occupancy: {occupancy}\n")
logFile.close()
writeNewValueIntoDataBase(f"'{datetime.now()}'", occupancy)