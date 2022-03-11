import sys
import time
import urllib.request
from datetime import datetime
import Adafruit_DHT
import mysqlx

rasbpy_id = "1"
if len(sys.argv) > 1:
    rasbpy_id = str(sys.argv[1])

sensor = Adafruit_DHT.DHT22
gpio = 4

connect_args = {
    'host': '<IP of the Compute Instance>',
    'port': 6448,
    'user': 'piday',
    'password': '',
    'ssl-mode': 'DISABLED',
    'schema': 'piday'
}


def connect():
    global external_ip
    global session
    global schema
    global tbl_temperature_history, tbl_humidity_history, tbl_publicip_history
    global col_devices
    external_ip = urllib.request.urlopen(
        'https://api.ipify.org').read().decode('utf8')
    session = mysqlx.get_session(**connect_args)
    schema = session.get_schema('piday')
    tbl_temperature_history = schema.get_table('temperature_history')
    tbl_humidity_history = schema.get_table('humidity_history')
    tbl_publicip_history = schema.get_table('publicip_history')
    col_devices = schema.get_collection('devices')


connect()

while(True):
    if not session.is_open():
        connect()
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    if humidity is not None and temperature is not None:
        # Find the device and its last ip
        res = col_devices.find("_id='{}'".format(rasbpy_id)).fields(
            '_id', 'publicip').execute()
        device = res.fetch_one()
        if device:
            old_public_ip = device['publicip']
        else:
            print("device with _id: {} not found !".format(rasbpy_id))
            print("sleeping 1 min...")
            time.sleep(60)
            continue
        patch_json = {}
        humidity_s = "{0:0.1f}%".format(humidity)
        temperature_s = "{0:0.1f}C".format(temperature)
        patch_json['humidity'] = humidity_s
        patch_json['temperature'] = temperature_s
        patch_json['publicip'] = external_ip
        patch_json['last_update'] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        print('Temp={}  Humidity={}'.format(temperature_s, humidity_s))
        col_devices.modify("_id='{}'".format(rasbpy_id)
                           ).patch(patch_json).execute()
        if old_public_ip != external_ip:
            tbl_publicip_history.insert(['device_id', 'ip_address']).values(
                rasbpy_id, external_ip).execute()
        tbl_temperature_history.insert(['time_stamp', 'device_id', 'value']).values(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), rasbpy_id, temperature).execute()
        tbl_humidity_history.insert(['time_stamp', 'device_id', 'value']).values(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), rasbpy_id, humidity).execute()
    else:
        print('Failed to get reading. Try again!')

    time.sleep(1)
