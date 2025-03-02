import automationhat

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

org = "influx-org"
url = "https://influx.foo.com"
token="xxx"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="greenhouse-1"

write_api = write_client.write_api(write_options=SYNCHRONOUS)



def water_plants():
    automationhat.relay.one.on()
    point = (
        Point("pump-1")
        .field("status", 1)
    )
    write_api.write(bucket=bucket, org=org, record=point)


    automationhat.relay.two.on()
    point = (
        Point("pump-2")
        .field("status", 1)
    )
    write_api.write(bucket=bucket, org=org, record=point)

    automationhat.relay.three.on()
    point = (
        Point("pump-3")
        .field("status", 1)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    print(f"pumps turned on at: {datetime.now().isoformat()}")


    time.sleep(5)
    
    automationhat.relay.one.off()
    print(f"pumps turned off at: {datetime.now().isoformat()}")
    point = (
        Point("pump-1")
        .field("status", 0)
    )
    write_api.write(bucket=bucket, org=org, record=point)

    automationhat.relay.two.off()
    point = (
        Point("pump-2")
        .field("status", 0)
    )
    write_api.write(bucket=bucket, org=org, record=point)

    automationhat.relay.three.off()
    point = (
        Point("pump-3")
        .field("status", 0)
    )
    write_api.write(bucket=bucket, org=org, record=point)

