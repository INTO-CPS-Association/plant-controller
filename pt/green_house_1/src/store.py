import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import yaml

def get_config():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

org = "influx-org"
url = "https://influx.foo.com"
token="xxx"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="greenhouse-1"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

if __name__ == "__main__":
    config = get_config()
    influxdb_config = config['services']['internal']['influxdb']
    url = influxdb_config['host'] + ":" + str(influxdb_config['port'])
    org = influxdb_config['org']
    bucket = influxdb_config['bucket']
    token = influxdb_config['token']
    print(url, org, bucket, token)