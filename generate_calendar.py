from bs4 import BeautifulSoup
import requests
import csv
import re
import datetime


RESULT_DIR = "gtfs"

content = requests.get("https://www.highspeed.mtr.com.hk/tc/ticket/timetable.html").text
soup = BeautifulSoup(content, "html.parser")
general_table = soup.find("table", attrs={"class": "general-table"})
short_haul_table = general_table.find("strong")
ymd = re.findall(r"\d+", short_haul_table.text)
date = ymd[0].zfill(4)+ymd[1].zfill(2)+ymd[2].zfill(2)

with open(f"{RESULT_DIR}/calendar.txt", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["service_id", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "start_date", "end_date"])
    writer.writerow(["normal", 1, 1, 1, 1, 1, 1, 1, datetime.date.today().strftime('%Y%m%d'), date])