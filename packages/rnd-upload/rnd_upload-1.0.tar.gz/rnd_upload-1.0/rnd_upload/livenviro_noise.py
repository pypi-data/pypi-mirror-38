import requests
from sqlalchemy import *
try:
    from .livenviro_util import *
except:
    from livenviro_util import *


def post_sample(sample, config):

    url = "{0}://{1}/api/poll".format(config["api_protocol"], config["api_ip"])
    #url = "{0}://{1}/api/poll".format(config["protocol"], config["rest_ip"])
    headers = {'content-type': "application/x-www-form-urlencoded"}

    payload = 	"X-API-KEY={0}" \
                 "&serial_number={1}" \
                 "&leq={2:.2f}" \
                 "&lmax={3:.2f}" \
                 "&lmin={4:.2f}" \
                 "&le={5:.2f}" \
                 "&ln1={6:.2f}" \
                 "&ln2={7:.2f}" \
                 "&ln3={8:.2f}" \
                 "&ln4={9:.2f}" \
                 "&ln5={10:.2f}" \
                 "&timestamp={11}" \
                 "&sd_card={12}" \
                 "&battery={13}" \
                 "&measuring={14}" \
                 "&charging={15}" \
                 "&system_error={16}" \
                 "&lp={17}" \
                 "&apv=0" \
                 "&lp_sub={18}" \
                 "&overload={19}" \
                 "&underrange={20}".format(config["api_key"], config["serial"], sample["leq"], sample["lmax"], sample["lmin"], sample["le"],
                                           sample["ln1"], sample["ln2"], sample["ln3"], sample["ln4"], sample["ln5"], sample["timestamp"].strftime('%Y/%m/%d %H:%M:%S'),
                                           sample["sd_card"], sample["battery"], sample["measuring"], sample["charging"], sample["system_error"],
                                           sample["lp"], sample["lp_sub"], sample["overload"], sample["underrange"])

    print(f_blue("\nPost payload:"))
    print(payload)
    print("\n")


    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    return response.text


def post_status(config):
    url = "{0}://{1}/api/status".format(config["api_protocol"], config["api_ip"])
    headers = {'content-type': "application/x-www-form-urlencoded"}

    data = {}

    data["X-API-KEY"] = config["api_key"]
    data["serial_number"] = config["serial"]
    # data["timestamp"] = sample["timestamp"].strftime('%Y.%m.%d-%H:%M:%S')
    data["sdcard"] = 27
    data["battery"] = 96.3
    data["measuring"] = 1
    data["mounted"] = 1
    data["charging"] = 13
    data["system_error"] = 0

    response = requests.request("POST", url, data=data, headers=headers, verify=False)
    return response.text


def display_sample(sample):
    data = [["Item", "Value"]]

    for key, value in sample.iteritems():
        data.append([key, value])

    table = AsciiTable(data)
    table.title = f_blue(" Sample ")

    print("\n")
    print(table.table)


def get_logs_between(station_id, start, end, metadata):
    logs = Table("station_log_{0}".format(station_id), metadata, autoload=True)

    query = logs.select(and_(logs.c.sample_timestamp >= start, logs.c.sample_timestamp < end)).order_by(logs.c.sample_timestamp)

    try:
        return list(query.execute())
    except:
        print("Failed to execute query")
        return []


def create_sample_csv(timestamp, csv_row):
    if csv_row is None:
        return sys.exit(0)

    sample = {
        "leq": float(csv_row[3]),
        "lmax": float(csv_row[5]),
        "lmin": float(csv_row[6]),
        "le": float(csv_row[4]),
        "ln1": float(csv_row[8]),
        "ln2": float(csv_row[9]),
        "ln3": float(csv_row[10]),
        "ln4": float(csv_row[11]),
        "ln5": float(csv_row[12]),
        "timestamp": timestamp,
        "sd_card": 100,
        "battery": 6,
        "measuring": 1,
        "charging": 13.5,
        "system_error": 0,
        "lp": 0,
        "lp_sub": 0,
        "overload": 0,
        "underrange": 0
    }

    return sample
