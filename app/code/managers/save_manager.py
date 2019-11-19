import os
import csv
from shutil import copyfile
from cv2 import imwrite
from values_manager import get_saved_path

headers = ["device_id", "latlon", "time_stamp", "plastic_count"]
#           14 days * 18 hours * minutes * seconds / prediction_interval of 60 seconds
row_limit = 14 * 18 * 60
trim = 0.5

class SaveManager:

	def __init__(self):
		# image stuff
		self.saved_path = get_saved_path()
		self.images_path = self.saved_path + "/images"
		# predictions stuff
		self.log_path = self.saved_path + "/prediction_log.csv"
		# create file if it doesn't exist
		if os.path.exists(self.log_path) == False:
			with open(self.log_path, mode = "w", newline = "") as f:
				w = csv.writer(f, delimiter = ",")
				w.writerow(headers)

	def update_log(self, data):
		with open(self.log_path, mode = "a", newline = "") as f:
			a = csv.writer(f, delimiter = ",")
			a.writerow(data)
		# trim log file if it exceeds the row limit
		if self._count_rows() > row_limit:
			self._trim_log(trim)

	def save_image(self, image, device_id, capture_time):
		save_path = self.images_path + "/" + device_id + "_" + capture_time + ".jpg"
		imwrite(save_path, image)

	def _count_rows(self):
		with open(self.log_path, mode = "r", newline = "") as f:
			r = csv.reader(f, delimiter = ",")
			try:
				count = sum(1 for row in r)
				return count
			except:
				return 0

	def _trim_log(self, percent_to_trim):
		# calculate rows to skip
		row_count = self._count_rows()
		skip = int(row_count * percent_to_trim)
		# make copy of log
		log_copy = "log_copy.csv"
		copyfile(self.log_path, log_copy)
		# read rows to keep from original
		keep_rows = []
		with open(self.log_path, mode = "r", newline = "") as f:
			r = csv.reader(f, delimiter = ",")
			for i, j in enumerate(r):
				if i < skip:
					continue
				keep_rows.append(j)
		# write keep rows into copy
		with open(log_copy, mode = "w", newline = "") as f:
			a = csv.writer(f, delimiter = ",")
			a.writerow(headers)
			for i in keep_rows:
				a.writerow(i)
		# overwrite log file with copy
		copyfile(log_copy, self.log_path)
		# delete copy
		os.remove(log_copy)
