# --------------------------------------------------------------------
# Script to post LEQ data
# It is using CPU load as Leq and Lmax values
# --------------------------------------------------------------------


import sys
import os
import ConfigParser
import datetime
import time

from terminaltables import AsciiTable
from sqlalchemy import *
from pytz import timezone, utc
import csv
try:
    from .livenviro import *
    from .livenviro_noise import *
    from .livenviro_util import *
except:
    from livenviro import *
    from livenviro_noise import *
    from livenviro_util import *


def main(config_filename):
    print("{0} {1}".format(f_blue("Configuration file:"), config_filename))

    config = read_config(config_filename)

    db = create_engine("mysql://{0}:{1}@{2}/{3}".format(config["db_username"], config["db_password"], config["db_ip"], config["db_name"]))
    metadata = MetaData(db)

    config["api_key"] = get_station_api_key(config["db_ip"], config["db_username"], config["db_password"], config["db_name"], config["station_id"])
    config["serial"] = get_station_serial_number(config["db_ip"], config["db_username"], config["db_password"], config["db_name"], config["station_id"])
    config["timezone"] = get_station_timezone(config["station_id"], metadata)

    station_timezone = timezone(config["timezone"])

    csv_file = []
    with open(config["csv_file"]) as file:
        r = csv.reader(file)
        for row in r:
            csv_file.append(row)
    # first row is headers, so initialise index at 1
    index = 1

    range_start = datetime.datetime.strptime(config["csv_range_start"], "%Y-%m-%d %H:%M:%S")
    config["csv_range_start"] = datetime.datetime(range_start.year, range_start.month, range_start.day,
                                                  range_start.hour, range_start.minute, 0, tzinfo=station_timezone)

    range_end = datetime.datetime.strptime(config["csv_range_end"], "%Y-%m-%d %H:%M:%S")
    config["csv_range_end"] = datetime.datetime(range_end.year, range_end.month, range_end.day, range_end.hour,
                                                range_end.minute, 0, tzinfo=station_timezone)

    logs = get_logs_between(config["station_id"], config["csv_range_start"].strftime("%Y-%m-%d %H:%M:%S"), config["csv_range_end"].strftime("%Y-%m-%d %H:%M:%S"), metadata)
    if len(logs) > 0:
        return sys.exit("There already are " + str(len(logs)) + " points stored between the requested CSV range")

    display_config(config)

    while True:
        table_data = [["Server", "Station"], [config["api_ip"], config["station_id"]]]
        table = AsciiTable(table_data)
        table.title = f_blue(" Station Info ")
        print("======================================================================================\n")

        print(table.table)

        if index >= len(csv_file):
            print('Done')
            return True

        # second column represents the time
        sample_time = datetime.datetime.strptime(csv_file[index][1], "%Y/%m/%d %H:%M:%S")
        local_timestamp = datetime.datetime(sample_time.year, sample_time.month, sample_time.day, sample_time.hour, sample_time.minute, 0, tzinfo=station_timezone)

        if (local_timestamp - config['csv_range_start']).total_seconds() >= 0 and (config['csv_range_end'] - local_timestamp).total_seconds() >= 0:
            sample = create_sample_csv(local_timestamp, csv_file[index])
        else:
            sample = None

        index += 1
        print('Current index: ' + str(index))

        if sample:
            display_sample(sample)

            response = post_sample(sample, config)
            print(response)

            response = post_status(config)
            print(response)


def read_config(config_filename):
    # Setup default configuration
    config = {
        "api_ip": "localhost",
        "api_protocol": "https",
        "station_id": 59,
        "api_key": None,
        "serial": None,
        "db_ip": "localhost",
        "db_username": "root",
        "db_password": "toor",
        "db_name": "acoustics",
        "timezone": None,
        "csv_file": "a.rnd",
        "csv_range_start": "2000-01-01 00:00:00",
        "csv_range_end": "2000-01-01 00:00:01"
    }

    config_parser = ConfigParser.SafeConfigParser()

    try:
        config_parser.read("./{0}".format(config_filename))

        if config_parser.has_option("Api", "api_ip"):
            config["api_ip"] = config_parser.get("Api", "api_ip")

        if config_parser.has_option("Api", "api_protocol"):
            config["api_protocol"] = config_parser.get("Api", "api_protocol")

        if config_parser.has_option("Database", "db_ip"):
            config["db_ip"] = config_parser.get("Database", "db_ip")

        if config_parser.has_option("Database", "db_username"):
            config["db_username"] = config_parser.get("Database", "db_username")

        if config_parser.has_option("Database", "db_password"):
            config["db_password"] = config_parser.get("Database", "db_password")

        if config_parser.has_option("Database", "db_name"):
            config["db_name"] = config_parser.get("Database", "db_name")

        if config_parser.has_option("Station", "station_id"):
            config["station_id"] = config_parser.getint("Station", "station_id")

        if config_parser.has_option("Station", "timezone"):
            config["timezone"] = config_parser.get("Station", "timezone")

        if config_parser.has_option("CSV", "csv_file"):
            config["csv_file"] = config_parser.get("CSV", "csv_file")

        if config_parser.has_option("CSV", "csv_range_start"):
            config["csv_range_start"] = config_parser.get("CSV", "csv_range_start")

        if config_parser.has_option("CSV", "csv_range_start"):
            config["csv_range_end"] = config_parser.get("CSV", "csv_range_end")

    except:
        print("Failed to parse config file")
        return sys.exit(0)

    return config
