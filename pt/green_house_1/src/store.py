import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write_api import WriteApi
import yaml

def get_config():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

def influx() -> WriteApi:
    config = get_config()
    influxdb_config = config['services']['internal']['influxdb']
    url = influxdb_config['host'] + ":" + str(influxdb_config['port'])
    org = influxdb_config['org']
    bucket = influxdb_config['bucket']
    token = influxdb_config['token']
    print(url, org, bucket, token)
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    write_api = write_client.write_api(write_options=SYNCHRONOUS)
    return write_api

if __name__ == "__main__":
    influx()
