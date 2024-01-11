import re
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver

load_dotenv()
# TODO: installation of python-dotenv, psycopg2, selenium

def loadSource():
    chrome = webdriver.Chrome()
    chrome.get("https://www.taminatherme.ch")
    return chrome.page_source 

source = loadSource()

def getOccupancy(sourceString):
    result = re.search(r"<span class=\"block font-bold\">([0-9]+)%</span>", sourceString)
    if result.group(1):
        return int(result.group(1))
    else:
        return -1

occupancy = getOccupancy(source)
if (occupancy < 0):
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


writeNewValueIntoDataBase(f"'{datetime.now()}'", occupancy)