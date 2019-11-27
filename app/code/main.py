# PUT AUTHORS, DATE AND PROGRAM DESCRIPTION HERE
#
#

######### IMPORT PACKAGES, SETTINGS AND VALUES #########

# import utility packages
import sys
import time
from datetime import datetime
import numpy as np
import cv2

# import manager functions
sys.path.insert(1, 'managers')
from db_manager import DBManager
from save_manager import SaveManager
from loc_manager import get_latlon, update_latlon
from values_manager import get_device, get_prediction

# import model
from model import countPlastic

######### SETUP #########

# load device settings
device = get_device()
device_id = device["id"]
latlon_method = device["latlon_method"]
latlon = device["latlon"]

# load prediction settings
prediction = get_prediction()
prediction_start = prediction["prediction_start"]
prediction_stop = prediction["prediction_stop"]
prediction_interval = prediction["prediction_interval"]

# load model
model = countPlastic()

# set up wireless communication
dbm = DBManager(latlon_method)

# set up save manager
sm = SaveManager()

######### MAIN LOOP #########


#import os
#file = 30


#fourcc = cv2.VideoWriter_fourcc(*'XVID')

#FILE_OUTPUT = 'output'+str(file)+'.avi'
#if os.path.isfile(FILE_OUTPUT):
#    os.remove(FILE_OUTPUT)
#out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 20.0, (int(device["frame_width"]), int(device["frame_height"])))
#current = 0

def get_mode():
    current_time = datetime.now()
    current_time = (current_time.hour * 100) + current_time.minute
    if current_time >= prediction_start and current_time <= prediction_stop:
        return True
    else:
        return False


while(True):
        # run prediction only if within predetermined timeframe
        mode = get_mode()
        if mode == True:
            time_keeper = time.time()
            # load camera settings
            camera = cv2.VideoCapture(0)
            camera.set(5, device["frame_rate"])
            camera.set(3, device["frame_width"])
            camera.set(4, device["frame_height"])
        while(mode):
            # capture frame
            ret, frame = camera.read()

            # get capture time
            capture_time = time.time()

            # get prediction
            ##count, boxes = model.update(frame)
            #model.displayResults(frame, count, boxes)
            #out.write(frame)
            #current = current + 1

            # upload predictions if time since last upload is greater than upload interval
            if capture_time - time_keeper > prediction_interval:
                    time_keeper = time_keeper + prediction_interval

                    # create prediction record
                    capture_time = datetime.fromtimestamp(capture_time).strftime("%Y-%m-%d %H:%M:%S")
                    data = [device_id, latlon, capture_time, count]

                    # append prediction to backup csv in case upload fails
                    sm.update_log(data)

                    # update table
                    dbm.update_table(data)
                    #FILE_OUTPUT = 'output'+str(file)+'.avi'
                    #if os.path.isfile(FILE_OUTPUT):
                    #    os.remove(FILE_OUTPUT)
                    #out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 20.0, (int(device["frame_width"]), int(device["frame_height"])))
                    #current = 0

                    #clear model every database update
                    model = countPlastic()
                    print("clear the model")
                    # TODO method for saving images locally

            # update mode
            mode = get_mode()

######### CLOSE #########
camera.release()
