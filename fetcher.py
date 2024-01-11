import re
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
load_dotenv()
chrome = webdriver.Chrome()
chrome.get("https://www.taminatherme.ch")
source = chrome.page_source
print(source)
result = re.search(r"<span class=\"block font-bold\">([0-9]+)%</span>", source)
occupancy = int(result.group(1))


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


writeNewValueIntoDataBase(f"'{datetime.now()}'", occupancy)