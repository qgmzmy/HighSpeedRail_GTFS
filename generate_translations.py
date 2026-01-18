import csv


RESULT_DIR = "gtfs"
STATION_NAME_SC = {
    "香港西九龍": "香港西九龙",
    "福田": "福田",
    "深圳北": "深圳北",
    "光明城": "光明城",
    "虎門": "虎门",
    "南沙北": "南沙北",
    "廣州南": "广州南"
}
STATION_NAME_EN = {
    "香港西九龍": "Hong Kong West Kowloon",
    "福田": "Futian",
    "深圳北": "Shenzhenbei",
    "光明城": "Guangmingcheng",
    "虎門": "Humen",
    "南沙北": "Nanshabei",
    "廣州南": "Guangzhounan"
}


with open(f"{RESULT_DIR}/translations.txt", "w", encoding="utf-8") as f:
    f.write("""table_name,field_name,language,translation,record_id
agency,agency_name,zh-CN,高速铁路,highspeed
agency,agency_fare_url,zh-CN,https://www.highspeed.mtr.com.hk/sc/main/buy-ticket.html,highspeed
stops,stop_name,zh-CN,香港西九龙,WEK
stops,stop_name,zh-CN,香港西九龙,WEK_pf
stops,stop_name,zh-CN,福田,FUT
stops,stop_name,zh-CN,福田,FUT_pf56
stops,stop_name,zh-CN,福田,FUT_pf78
stops,stop_name,zh-CN,深圳北,SZB
stops,stop_name,zh-CN,深圳北,SZB_pf
stops,stop_name,zh-CN,光明城,GMC
stops,stop_name,zh-CN,光明城,GMC_pf1
stops,stop_name,zh-CN,光明城,GMC_pf2
stops,stop_name,zh-CN,虎门,HUM
stops,stop_name,zh-CN,虎门,HUM_pf12
stops,stop_name,zh-CN,虎门,HUM_pf34
stops,stop_name,zh-CN,南沙北,QIS
stops,stop_name,zh-CN,南沙北,QIS_pf1
stops,stop_name,zh-CN,南沙北,QIS_pf2
stops,stop_name,zh-CN,广州南,GZN
stops,stop_name,zh-CN,广州南,GZN_pf
routes,route_short_name,zh-CN,高速铁路,XRL
routes,route_long_name,zh-CN,广深港高速铁路,XRL
attributions,organization_name,zh-CN,香港铁路有限公司,MTR
""")


with open(f"{RESULT_DIR}/trips.txt", "r", encoding="utf-8") as f:
    reader = csv.reader(f)

    trips = list(reader)[1:]


with open(f"{RESULT_DIR}/translations.txt", "a", encoding="utf-8") as f:
    writer = csv.writer(f)

    for trip in trips:
        table_name = "trips"
        field_name = "trip_headsign"
        language = "zh-CN"
        translation = STATION_NAME_SC[trip[3]]
        record_id = trip[2]
        writer.writerow([table_name, field_name, language, translation, record_id])


with open(f"{RESULT_DIR}/translations.txt", "a", encoding="utf-8") as f:
    f.write("""table_name,field_name,language,translation,record_id
agency,agency_name,en,High Speed Rail,highspeed
agency,agency_fare_url,en,https://www.highspeed.mtr.com.hk/sc/main/buy-ticket.html,highspeed
stops,stop_name,en,Hong Kong West Kowloon,WEK
stops,stop_name,en,Hong Kong West Kowloon,WEK_pf
stops,stop_name,en,Futian,FUT
stops,stop_name,en,Futian,FUT_pf56
stops,stop_name,en,Futian,FUT_pf78
stops,stop_name,en,Shenzhenbei,SZB
stops,stop_name,en,Shenzhenbei,SZB_pf
stops,stop_name,en,Guangmingcheng,GMC
stops,stop_name,en,Guangmingcheng,GMC_pf1
stops,stop_name,en,Guangmingcheng,GMC_pf2
stops,stop_name,en,Humen,HUM
stops,stop_name,en,Humen,HUM_pf12
stops,stop_name,en,Humen,HUM_pf34
stops,stop_name,en,Nanshabei,QIS
stops,stop_name,en,Nanshabei,QIS_pf1
stops,stop_name,en,Nanshabei,QIS_pf2
stops,stop_name,en,Guangzhounan,GZN
stops,stop_name,en,Guangzhounan,GZN_pf
routes,route_short_name,en,High Speed Rail,XRL
routes,route_long_name,en,Guangzhou-Shenzhen-Hong Kong High Speed Rail,XRL
attributions,organization_name,en,MTR Corporation Limited,MTR
""")


with open(f"{RESULT_DIR}/translations.txt", "a", encoding="utf-8") as f:
    writer = csv.writer(f)

    for trip in trips:
        table_name = "trips"
        field_name = "trip_headsign"
        language = "en"
        translation = STATION_NAME_EN[trip[3]]
        record_id = trip[2]
        writer.writerow([table_name, field_name, language, translation, record_id])
