import requests, csv


STATION_NAME = {
    "WEK": "香港西九龍",
    "FUT": "福田",
    "SZB": "深圳北",
    "GMC": "光明城",
    "HUM": "虎門",
    "QIS": "南沙北",
    "GZN": "廣州南",
}


def trip_info():
    trips = []
    resp = requests.get("https://www.highspeed.mtr.com.hk/res/content/app/XRL_content_Timetable.json")
    resp.encoding = "utf-8-sig"
    timetable = resp.json()
    trains = timetable["routes"]
    mtr_trips = []

    for train in trains:
        key = list(train.keys())[0]
        train = train[key]
        if train["train_model"] == "M":
            mtr_trips.append(train)


    for train in mtr_trips:
        route_id = "XRL"
        service_id = "normal"
        trip_id = train["id"]
        trip_headsign = STATION_NAME[train["end_station_code"]]
        trip_short_name = train["id"]
        direction_id = 1 if train["end_station_code"] == "WEK" else 0
        wheelchair_accessible = 1
        cars_allowed = 2
        trip = [route_id, service_id, trip_id, trip_headsign, trip_short_name, direction_id, wheelchair_accessible, cars_allowed]
        trips.append(trip)

    return trips



if __name__ == "__main__":
    RESULT_DIR = "gtfs"

    with open(f"{RESULT_DIR}/trips.txt", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["route_id", "service_id", "trip_id", "trip_headsign", "trip_short_name", "direction_id", "wheelchair_accessible", "cars_allowed"])
        trips = trip_info()
        for trip in trips:
            writer.writerow(trip)
