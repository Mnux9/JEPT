import configparser
from pathlib import Path
from astroquery.jplhorizons import Horizons
import matplotlib.pyplot as plt
import numpy as np


config = configparser.ConfigParser()

config.read('config.ini')



with open('temp.txt','w') as f: #Clears the temp.txt file
                f.write("")

print(config.get('LOC','Latitude'), config.get('LOC','Longitude'), config.get('LOC','Altitude'))
print(config.get('SCID','spacecraft'))


while True:
    
    #This code processes epheris data from JPL horizons
    #This code was written by Wyattaw and modified by mnux

    # set your lat/long/elevation
    home = {'lat': float(config.get('LOC','Latitude')), 'lon': float(config.get('LOC','Longitude')), 'elevation': float(config.get('LOC','Altitude'))}
    # set minimum el to search above
    minEl = 0
    # create object to query horizons website
    # prediction of the whole pass/es
    

    obj = Horizons(id= config.get('SCID','Spacecraft'),
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

            print(T,A,E)

            with open('temp.txt','w') as f: #Writes the values to the tepm.txt file                

                f.write(str(A))
                f.write(",")
                f.write(str(E))
                f.write("\n")

time.sleep(3)

           
       



