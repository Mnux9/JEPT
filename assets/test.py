from astroquery.jplhorizons import Horizons
import matplotlib.pyplot as plt
import numpy as np
# set your lat/long/elevation
home = {'lat': 50, 'lon': 16, 'elevation': 0}
# set minimum el to search above
minEl = -90
# set time step
step = '3m'
# create object to query horizons website
obj = Horizons(id='JWST',
               location=home,
               epochs=None)
# get ephemris from query
eph = obj.ephemerides()
# make 3 lists for time, az, and el. Then print all of them together,
# so the az el and time all line up. Only print when object is above
# horizon
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
        print(A, E)
# change az from deg to rad
polarAzList = []
for p in azList:
    polarAzList.append(np.deg2rad(p))

# plot az el graph
# need to find way to include time
fig = plt.figure()
ax = plt.subplot(121)
ax.set_ylim(0, 90)
ax.set_xlim(0, 360)
ax.set_ylabel('Elevation')
ax.set_xlabel('Azimuth')
ax.set_xticks(np.arange(0, 360, 45))
ax.grid(True)
ax.plot(azList, elList)

# make polar graph
ax2 = plt.subplot(122, projection='polar')
# make 90deg  in middle, 0deg on outside
ax2.set_rlim(bottom=90, top=0)
#rotate so 0deg AZ is on top
ax2.set_theta_zero_location('N')
# make theta increase clockwise
ax2.set_theta_direction(-1)
ax2.plot(polarAzList, elList)

fig.show()
