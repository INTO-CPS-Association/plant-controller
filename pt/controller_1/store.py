import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
import yaml
from typing import Tuple

class InfluxDBStore:
    def __init__(self):
        config = self.get_config()
        config = config["services"]["internal"]["influxdb"]
        self._org = config["org"]
        self._url = config["url"]
        self._token = config["token"]
        self._bucket = config["bucket"]
        #print(self._org, self._url, self._token, self._bucket)
        write_client = influxdb_client.InfluxDBClient(
            url=self._url, token=self._token, org=self._org
        )
        self._write_api = write_client.write_api(
            write_options=SYNCHRONOUS
        )

    def get_config(self) -> dict:
        with open("config/config.yaml", "r") as file:
            data = yaml.safe_load(file)
        return data

    def write(self, record: Point) -> None:
        """
        Write a single data point to InfluxDB.
        """
        try:
            self._write_api.write(bucket=self._bucket, org=self._org, record=record)
            print(f"Successfully wrote point '{record.to_line_protocol()}' to the bucket {self._bucket}.")
        except InfluxDBError as e:
            print(f"Failed to write point '{record.to_line_protocol()}' with exception: {e.message}")
            print(f"Error Status Code: {e.status}")
            print(f"Error Message: {e.body}")
            print(f"Error Headers: {e.headers}")

