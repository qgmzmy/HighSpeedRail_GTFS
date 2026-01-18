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

with open(f"{RESULT_DIR}/feed_info.txt", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["feed_publisher_name", "feed_publisher_url", "feed_lang", "default_lang", "feed_start_date", "feed_end_date", "feed_version", "feed_contact_email"])
    writer.writerow(["qgmzmy", "https://blog.qgmzmy.me/", "zh-HK", "zh-CN", datetime.date.today().strftime('%Y%m%d'), date, input("feed version: "), "qgmzmy114514@gmail.com"])