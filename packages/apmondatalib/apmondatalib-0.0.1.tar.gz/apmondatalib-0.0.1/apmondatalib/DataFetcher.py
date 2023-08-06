import pymongo
import datetime
from enum import IntEnum


class SensorType(IntEnum):
    Humidity = 1
    Temperature = 2
    Light = 3
    Motion = 4


def create_raw_data_fetcher(host, port, database, sensor_id, time_offset=9):
    return SensorRawDataFetcher(host, port, database, sensor_id, time_offset)


class RawData:
    id = ""
    sensor_id = ""
    type = 0
    value = 0.0

    def __init__(self, sensor_id, type, json):
        self.sensor_id = sensor_id
        self.type = type
        self.id = json["_id"]
        self.value = json["value"]

    def __str__(self):
        return "{ RawData: _id = %s, sensor_id = %s, type = %s, value = %f }" % (
            self.id, self.sensor_id, self.type, self.value)

    def __repr__(self):
        return "{ RawData: _id = %s, sensor_id = %s, type = %s, value = %f }" % (
            self.id, self.sensor_id, self.type, self.value)


def convert_cursor_to_raw_data(sensor_id, sensor_type, cursor):
    result = []
    for x in cursor:
        result.append(RawData(sensor_id, sensor_type, x))

    return result


def calculate_skip_position(page_number, page_size):
    return page_size * (page_number - 1)


class SensorRawDataFetcher:
    mongo = None
    collection = None

    sensor_id = ""
    timeOffset = 0

    default_field_visibility = {"_id": 1, "value": 1, "timestamp": 1}

    def __init__(self, host, port, database, sensor_id, time_offset):
        self.host = host
        self.port = port
        self.database = database
        self.mongo = pymongo.MongoClient('mongodb://%s:%d/' % (host, port))
        self.collection = self.mongo[database]["sensor_data"]

        self.sensor_id = sensor_id
        self.time_offset = time_offset

    def read(self, sensor_type, page_size, page_number):
        skips = calculate_skip_position(page_number, page_size)
        return convert_cursor_to_raw_data(
            self.sensor_id, sensor_type,
            self.collection.find({"sensorId": self.sensor_id, "type": sensor_type.value},
                                 self.default_field_visibility).skip(skips).limit(page_size))

    def read_in_range(self, sensor_type, date, page_size, page_number):
        print date.day
        skips = calculate_skip_position(page_number, page_size)
        return convert_cursor_to_raw_data(
            self.sensor_id, sensor_type,
            self.collection.find({"sensorId": self.sensor_id, "type": sensor_type.value},
                                 self.default_field_visibility).skip(skips).limit(page_size))

    def read_humidity(self, sensor_id, page_size, page_number):
        return self.read(sensor_id, SensorType.Humidity, page_size, page_number)

    def read_temperature(self, sensor_id, page_size, page_number):
        return self.read(sensor_id, SensorType.Temperature, page_size, page_number)

    def read_light(self, sensor_id, page_size, page_number):
        return self.read(sensor_id, SensorType.Light, page_size, page_number)

    def read_motion(self, sensor_id, page_size, page_number):
        return self.read(sensor_id, SensorType.Motion, page_size, page_number)
