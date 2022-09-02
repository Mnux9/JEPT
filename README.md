# JEPT
Nasa JPL EPHEMRIS PROCESSING TOOL


This is a tool for viewing azimuth and eleveation of selected spacecraft from JPL ephermis data based on entered QTH location.

The ephems are pulled live from Nasa JPL so it wont work without interntet connection for now.

Keep in mind that this code is still not done, needs a lot of changes and features but it somewhat works.

![shutter tap](https://github.com/Mnux9/JEPT/blob/main/Images/UI.png)

# How to run:

dependencies: pysimplegui, pathlib, datetime, astroquery, numpy, configpraser

run on linux: ```python3 jept.py```

configure settings

and click Run!


# To do:

Add offline support

Add rotator support


# To fix:

Make the Prediction end time in UTC too, in local for now

✅fix the lat/long GUI settings (thanks Wyattaw!)

