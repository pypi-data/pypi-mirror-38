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
    time_offset = 0

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

    def count(self, sensor_type):
        return self.collection.count({"sensorId": self.sensor_id, "type": sensor_type.value})

    #def count_total(self):
    #    return self.collection.count()

    def count_total_pages(self, sensor_type, page_size):
        total_count = self.count(sensor_type)
        page_count = total_count / page_size
        if total_count % page_size:
            page_count += 1
        return page_count

    def read_in_range(self, sensor_type, date, page_size, page_number):
        print date.day
        skips = calculate_skip_position(page_number, page_size)
        return convert_cursor_to_raw_data(
            self.sensor_id, sensor_type,
            self.collection.find({"sensorId": self.sensor_id, "type": sensor_type.value},
                                 self.default_field_visibility).skip(skips).limit(page_size))

    def read_humidity(self, page_size, page_number):
        return self.read(SensorType.Humidity, page_size, page_number)

    def read_temperature(self,  page_size, page_number):
        return self.read(SensorType.Temperature, page_size, page_number)

    def read_light(self, page_size, page_number):
        return self.read(SensorType.Light, page_size, page_number)

    def read_motion(self, page_size, page_number):
        return self.read(SensorType.Motion, page_size, page_number)

    def count_humidity(self):
        return self.count(SensorType.Humidity)

    def count_temperature(self):
        return self.count(SensorType.Temperature)

    def count_light(self):
        return self.count(SensorType.Light)

    def count_motion(self):
        return self.count(SensorType.Motion)

    def count_total_humidity_pages(self, page_size):
        return self.count_total_pages(SensorType.Humidity, page_size)

    def count_total_temperature_pages(self, page_size):
        return self.count_total_pages(SensorType.Temperature, page_size)

    def count_total_light_pages(self, page_size):
        return self.count_total_pages(SensorType.Light, page_size)

    def count_total_motion_pages(self, page_size):
        return self.count_total_pages(SensorType.Motion, page_size)