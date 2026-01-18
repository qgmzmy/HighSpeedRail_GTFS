from generate_trips import trip_info
from tenacity import retry
import datetime, requests, csv, time


TRAIN_CODES = list(map(lambda x: x[2], trip_info()))
DATE = datetime.date.today()


def get_stop_id(station: str, direction: int) -> str:
    match station:
        case "香港西九龙":
            return "WEK_pf"
        case "福田":
            return "FUT_pf56" if direction else "FUT_pf78"
        case "深圳北":
            return "SZB_pf"
        case "光明城":
            return "GMC_pf2" if direction else "GMC_pf1"
        case "虎门":
            return "HUM_pf34" if direction else "HUM_pf12"
        case "南沙北":
            return "QIS_pf2" if direction else "QIS_pf1"
        case "广州南":
            return "GZN_pf"


@retry
def http_get(url: str) -> dict:
    return requests.get(url).json()


def stop_times_info(write: bool = False, result_dir: str = "gtfs", sleep: float = 0.0) -> list:
    stop_times = []
    if write:
        with open(f"{result_dir}/stop_times.txt", "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "timepoint"])

    for train_code in TRAIN_CODES:
        url = f"https://search.12306.cn/search/v1/train/search?keyword={train_code}&date={DATE.strftime('%Y%m%d')}"
        resp = http_get(url)
        data = resp["data"][0]
        train_no = data["train_no"]

        url = f"https://kyfw.12306.cn/otn/queryTrainInfo/query?leftTicketDTO.train_no={train_no}&leftTicketDTO.train_date={DATE.strftime('%Y-%m-%d')}&rand_code="
        resp = http_get(url)
        data = resp["data"]["data"]


        for stop in data:
            trip_id = train_code
            arrival_time = stop["start_time"]+":00" if stop["running_time"] == "00:00" else stop["arrive_time"]+":00"
            departure_time = stop["start_time"]+":00" if stop["start_time"] >= stop["arrive_time"] else stop["arrive_time"]+":00"
            stop_id = get_stop_id(stop["station_name"], int(train_code[-1])%2)
            stop_sequence = int(stop["station_no"])
            timepoint = 1
            stop_time = [trip_id, arrival_time, departure_time, stop_id, stop_sequence, timepoint]
            stop_times.append(stop_time)
            if write:
                with open(f"{result_dir}/stop_times.txt", "a", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(stop_time)
        print(train_code, "done")
        time.sleep(sleep)

    return stop_times


if __name__ == "__main__":
    RESULT_DIR = "gtfs"

    stop_times = stop_times_info(write=True, result_dir=RESULT_DIR, sleep=5)
