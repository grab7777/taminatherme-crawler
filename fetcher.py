import re
import os
import psycopg2

from dotenv import load_dotenv
from datetime import datetime
from pyppeteer import launch
import asyncio

load_dotenv()

async def loadSource():
    browser = await launch(headless=True,args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-software-rasterizer', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.goto("https://www.taminatherme.ch")
    html_content = await page.content()
    await page.close()
    await browser.close()
    return html_content


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
    pwFile  = open("/run/secrets/db_password", "r")
    DB_PASSWORD = pwFile.readline()
    pwFile.close()
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
    logFile = open("/cron_task.log", "a")
    logFile.write(f"Date: {timestamp}\t Occupancy: {occupancy}\n")
    logFile.close()
    # TODO: Error handling

occupancy = getOccupancy(source)
writeNewValueIntoDataBase(f"'{datetime.now()}'", occupancy)