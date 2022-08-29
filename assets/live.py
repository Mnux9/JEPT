import configparser
from pathlib import Path
import datetime
from datetime import timedelta
from astroquery.jplhorizons import Horizons
import matplotlib.pyplot as plt
import numpy as np


config = configparser.ConfigParser()

config.read('config.ini')




with open('temp.txt','w') as f: #Clears the temp.txt file
                f.write("")


while True:
    
    #This code processes epheris data from JPL horizons
    #This code was written by Wyattaw and modified by mnux

    # set your lat/long/elevation
    home = {'lat': 50, 'lon': 16, 'elevation': 0}
    # set minimum el to search above
    minEl = 0
    # create object to query horizons website
    # prediction of the whole pass/es
    

    obj = Horizons(id= 'SOHO',
                    location=home,
                    epochs=None)
        # get ephemris from query
    eph = obj.ephemerides()
        # make 3 lists for time, az, and el. Then print all of them together,
        # so the az el and time all line up. Only print when object is above horizon
    azList = []
    elList = []
    timeList = []
    for p in eph['datetime_str']:
        timeList.append(p)
    for p in eph['AZ']:
        azList.append(p)
    for p in eph['EL']:
        elList.append(p)
    for (T, A, E) in zip(timeList, azList, elList):
        if E >= minEl:
            with open('temp.txt','w') as f: #Writes the values to the tepm.txt file

                print(A,E)

                f.write(str(A))
                f.write(",")
                f.write(str(E))
                f.write("\n")

time.sleep(4)

           
       



