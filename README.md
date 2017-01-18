# iot_ble_analytic

Read from MQTT broker RSSI values send by BLE devices and try to determine positions of all BLE devices.

In package convert, it only does the conversion of incoming data (either from MQTT or from text file) to a new data structure which is the entry point for position calculation
In package position, do data conversion from incoming data (MQTT), calculate position and display it. Data conversion is done the old way.