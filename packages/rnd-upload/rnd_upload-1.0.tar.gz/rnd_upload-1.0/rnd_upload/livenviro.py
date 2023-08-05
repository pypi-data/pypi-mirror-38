import MySQLdb
from sqlalchemy import *


def get_station_timezone(station_id, metadata):
    """
    Queries the database for station timezone using the serial number

    :param station_id: station ID number
    :param metadata: Alchemy SQL metadata object
    :returns: station timezone
    """
    station_table = Table("station", metadata, autoload=True)

    query = station_table.select(station_table.c.id == station_id)
    result = query.execute()
    keys = result.keys()
    result = list(result)

    if len(result) > 0:
        timezone_index = keys.index("timezone")
        timezone = result[0][timezone_index]
    else:
        timezone = "Europe/London"

    return timezone


def get_station_api_key(ip, username, password, database, station_id):
    """
    Queries database for station API key. Legacy -> Doesn't use SQL Alchemy.

    :param str ip: Server's ip
    :param str username: MySQL username
    :param str password: MySQL password
    :param str database: MySQL database name
    :param str station_id: station ID number
    :returns: station API key
    """
    try:
        db = MySQLdb.connect(ip, username, password, database)
        cursor = db.cursor()
    except:
        print("Failed to connect to database (get_api_key)")
        return None


    query = "SELECT api_key.key FROM monitor JOIN api_key ON api_key.id = monitor.api_key_id where station_id = {0};".format(station_id);

    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print("Failed to run query (get_api_key)")
        return None

    try:
        keys = list(cursor.fetchall())
        if len(keys) > 0:
            key = keys[0][0]
        else:
            key = None
    except:
        print("Unable to fecth data (api_key)")
        return None

    return key


def get_station_serial_number(ip, username, password, database, station_id):
    """
    Queries database for station serial number. Legacy -> Doesn't use SQL Alchemy.

    :param str ip: Server's ip
    :param str username: MySQL username
    :param str password: MySQL password
    :param str database: MySQL database name
    :param str station_id: station ID number
    :returns: station serial key/number
    """
    try:
        db = MySQLdb.connect(ip, username, password, database)
        cursor = db.cursor()
    except:
        print("Failed to connect to database (get_api_key)")
        return None


    query = "SELECT serial FROM monitor where station_id = {0};".format(station_id);

    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print("Failed to run query (get_serial_number)")
        return None

    try:
        monitors = list(cursor.fetchall())
        if len(monitors) > 0:
            serial = monitors[0][0]
        else:
            serial = None
    except:
        print("Unable to fecth data (get_serial_number)")
        return None

    return serial
