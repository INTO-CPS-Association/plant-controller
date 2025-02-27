# Updates

## 27-Feb-2025

The demo setup is running with a single motor.
Two soil moisture sensors are connected to Adafruit
8-ch multiplexer as follows:

port 6 and 7 --> soil moisture sensors

With this setup, execute three programs.

1. sensehat.py
2. controller.py

The data is being written to InfluxDB database with the following details.

```txt
URL: https://dtl-server-2.st.lab.au.dk
Org: TestUserDTaaS
Bucket: greenhouse-1
```
