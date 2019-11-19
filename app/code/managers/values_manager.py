# for getting imports from local .py files
import os
import sys
from pathlib import Path
import json

def get_root_path():
	path = os.path.dirname(os.path.abspath(__file__))
	path = Path(path).parents[1]
	path = str(path)
	return path

def get_saved_path():
	return get_root_path() + "/saved"

def get_values_path():
	return get_root_path() + "/conf/values.json"

def get_data():
	return json.load(open(get_values_path()))

def get_category(category):
	data = get_data()
	return data[category]

def get_value(category, key):
	category = get_category(category)
	return category[key]

def update_value(category, key, update):
	path = get_values_path()
	with open(path, "r") as f:
		data = json.load(f)
		data[category][key] = update
	with open(path, "w") as f:
		f.write(json.dumps(data, indent = 4))

def get_device():
	return get_category("device")

def get_prediction():
	return get_category("prediction")

def get_database():
	return get_category("database")
