# JEPT - JPL Ephemeris Processing Tool

This is a tool for viewing, predicting and graphing the azimuth and elevation of selected spacecraft from the JPL ephermis data based on the entered QTH location. The ephems are pulled live from the JPL Horizons system, so the software will not run without an internet connection for now.

Keep in mind that this code is still not done; it still needs a lot of changes and features but it somewhat works.

![shutter tap](https://github.com/Mnux9/JEPT/blob/main/Images/UI.png)

# How to run:

This software depends on these python dependencies: `pysimplegui, pathlib, datetime, astroquery, numpy, configparser`

Then, simply ```python3 jept.py``` for any *nix system. 

# To do (internal use):

- Add offline support

- Add rotator support

- Make the Prediction end time in UTC too, the current is in **local** for now


