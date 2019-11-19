# code to to manage retrieval of latitude, longitude location
import requests
import json
import time

from values_manager import get_device, update_value
from lte_manager import get_gps_power, turn_gps_on, turn_gps_off, get_gps_loc

GPS_WAIT = 120
GPS_PAUSE = 10

def get_latlon_method():
	return get_device()["latlon_method"]

def get_latlon():
	return get_device()["latlon"]

def get_loc_name():
	return get_device()["location_name"]

def update_latlon_method(update):
	update_value("device", "latlon_method", update)

def update_latlon(user_input = None):
	latlon_method = get_latlon_method()
	if latlon_method == "USER":
		if user_input == None:
			print("No user input specified. Latlon set to \"None\"")
		update_value("device", "latlon", user_input)
	elif latlon_method == "WIFI":
		update_value("device", "latlon", _get_latlon_wifi())
	elif latlon_method == "GPS":
		update_value("device", "latlon", _get_latlon_gps())
	else:
		print("Update method is unrecognized. No update made.")

def update_loc_name(update):
	update_value("device", "location_name", update)

def _get_latlon_wifi():
	url = 'https://extreme-ip-lookup.com/json/'
	r = requests.get(url)
	data = json.loads(r.content.decode())
	return data.get("lat") + "," + data.get("lon")

def _get_latlon_gps():
	if get_gps_power() == 0:
		turn_gps_on()
	latlon = None
	start_time = time.time()
	while True:
		time.sleep(GPS_PAUSE)
		latlon = get_gps_loc()
		current_time = time.time()
		print("Time: " + str(current_time - start_time) + "    ,    Latlon: " + str(latlon))
		# if latlon found
		if latlon != None:
			print("Latitude, longitude found: " + latlon)
			break
		# if exceeds wait time
		if (current_time - start_time >= GPS_WAIT):
			print("Exceeded wait time of " + str(GPS_WAIT) + " seconds.")
			break
	turn_gps_off()
	return latlon
