import re
import os
import psycopg2

from playwright.sync_api import sync_playwright

from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

debug = True if os.getenv("DEBUG") else False
logFilePath = os.getenv("LOG_FILE_PATH") or "/fetcher.log"


def loadSource():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # browser = await launch(headless=True,args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-software-rasterizer', '--disable-setuid-sandbox'])
        page = browser.new_page()
        url = os.getenv("URL_TO_CRAWL") or "https://www.taminatherme.ch"
        page.goto(url)
        # TODO: wait for occupancy to load
        time.sleep(2)
        title = page.title()
        html_content = page.content()
        browser.close()
        if debug:
            print("loaded website:", title, url)
            with open("./temp/content.html", "w", encoding="utf-8") as writer:
                writer.write(html_content)
                writer.close()
        return html_content


def getOccupancy(sourceString):
    customRegex = (
        os.getenv("CUSTOM_REGEX") or r"<span class=\"block font-bold\">([0-9]+)%</span>"
    )
    result = re.search(customRegex, sourceString)
    if debug:
        print("regex used:", customRegex)
        print(f"Regex result\n{result}")
    if (
        result
        and result.group(1)
        and int(result.group(1)) >= 0
        and int(result.group(1)) <= 100
    ):
        print("Occupancy: " + result.group(1))
        return int(result.group(1))
    else:
        print("Could not find occupancy on Website")
        exit(0)


def writeNewValueIntoDataBase(timestamp, occupancy):
    DB_USER = os.getenv("DB_USER")
    pwFilePath = os.getenv("PW_FILE_PATH") or "/run/secrets/db_password"
    pwFile = open(pwFilePath, "r")
    DB_PASSWORD = pwFile.readline().replace("\n", "")
    pwFile.close()
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_DATABASE_NAME = os.getenv("DB_DATABASE_NAME")
    try:
        connection = psycopg2.connect(
            database=DB_DATABASE_NAME,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS occupancy(
                    timestamp timestamp PRIMARY KEY,
                    occupancy integer NOT NULL,
                    CONSTRAINT occ_valid CHECK (occupancy >= 0 AND occupancy <= 100));
                    """
        )
        cursor.execute(
            f"INSERT INTO occupancy(timestamp, occupancy) VALUES({timestamp},{occupancy})"
        )
        connection.commit()
    except:
        logFile = open(logFilePath, "a")
        logFile.write(
            f"Date: {timestamp}\t Error: could not write into DB, occupancy: {occupancy}\n"
        )
        logFile.close()
        connection.rollback()
        connection.close()
    logFile = open(logFilePath, "a")
    logFile.write(f"Date: {timestamp}\t Occupancy: {occupancy}\n")
    logFile.close()


source_code = loadSource()
occupancy = getOccupancy(source_code)
writeNewValueIntoDataBase(f"'{datetime.now()}'", occupancy)
