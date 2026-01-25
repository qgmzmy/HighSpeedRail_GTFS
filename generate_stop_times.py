from generate_trips import trip_info
from tenacity import retry
import datetime, requests, csv, time


DATE = datetime.date.today()


def get_service_date(calendar_path: str = "gtfs/calendar.txt") -> dict:
    """从 calendar.txt 读取每个 service 对应最临近且不早于今天的活跃日期"""
    service_dates = {}
    today = datetime.date.today()
    
    with open(calendar_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_id = row['service_id']
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            start_date = datetime.datetime.strptime(row['start_date'], '%Y%m%d').date()
            end_date = datetime.datetime.strptime(row['end_date'], '%Y%m%d').date()
            
            # 找到最接近但不早于今天的被标记为1的日期
            closest_date = None
            
            current_date = max(start_date, today)  # 从今天或 start_date 开始
            while current_date <= end_date:
                day_name = days[current_date.weekday()]
                if row[day_name] == '1':
                    closest_date = current_date
                    break  # 找到第一个符合条件的就是最近的
                current_date += datetime.timedelta(days=1)
            
            if closest_date:
                service_dates[service_id] = closest_date
    
    return service_dates


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
    
    # 读取服务日期映射
    service_dates = get_service_date(f"{result_dir}/calendar.txt")
    
    # 缓存已查询过的 trip_id 的时刻表（每个车次只查询一次）
    queried_schedules = {}
    
    if write:
        with open(f"{result_dir}/stop_times.txt", "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "timepoint"])

    # 读取 trips.txt
    with open(f"{result_dir}/trips.txt", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        trips_list = list(reader)
    
    for trip in trips_list:
        trip_id = trip['trip_id']
        service_id = trip['service_id']
        
        # 获取该 service 对应的查询日期
        query_date = service_dates.get(service_id)
        if not query_date:
            print(f"Warning: No valid date found for service {service_id}")
            continue
        
        # 如果该车次还没查询过，则查询
        if trip_id not in queried_schedules:
            url = f"https://search.12306.cn/search/v1/train/search?keyword={trip_id}&date={query_date.strftime('%Y%m%d')}"
            resp = http_get(url)
            data = resp["data"][0]
            train_no = data["train_no"]

            url = f"https://kyfw.12306.cn/otn/queryTrainInfo/query?leftTicketDTO.train_no={train_no}&leftTicketDTO.train_date={query_date.strftime('%Y-%m-%d')}&rand_code="
            resp = http_get(url)
            queried_schedules[trip_id] = resp["data"]["data"]
            print(f"{trip_id} (service: {service_id}, date: {query_date}) queried")
            time.sleep(sleep)
        
        # 使用缓存的时刻表数据
        data = queried_schedules[trip_id]
        
        for stop in data:
            arrival_time = stop["start_time"]+":00" if stop["running_time"] == "00:00" else stop["arrive_time"]+":00"
            departure_time = stop["start_time"]+":00" if stop["start_time"] >= stop["arrive_time"] else stop["arrive_time"]+":00"
            stop_id = get_stop_id(stop["station_name"], int(trip_id[-1])%2)
            stop_sequence = int(stop["station_no"])
            timepoint = 1
            stop_time = [trip_id, arrival_time, departure_time, stop_id, stop_sequence, timepoint]
            stop_times.append(stop_time)
            if write:
                with open(f"{result_dir}/stop_times.txt", "a", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(stop_time)

    return stop_times


if __name__ == "__main__":
    RESULT_DIR = "gtfs"

    stop_times = stop_times_info(write=True, result_dir=RESULT_DIR, sleep=5)
