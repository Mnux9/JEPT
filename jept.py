import PySimpleGUI as sg
from pathlib import Path
import datetime
from datetime import timedelta


timestart = datetime.datetime.now()
timestart = timestart.strftime("%Y-%m-%d %H-%M-%S")

timeend = datetime.datetime.now() + timedelta(hours=24)
timeend = timeend.strftime("%Y-%m-%d %H-%M-%S")


#Settings window
def settings_window(settings):
    #Settings layout
    layout = [

        [sg.Text("Location:")],
        [sg.Text("Latitude:"), sg.Text("Longitude:"), sg.Text("Altitude:")],
        [sg.Input(settings["LOC"]["latitude"], s=8, key="-LAT-"),
         sg.Input(settings["LOC"]["longitude"], s=8, key="-LON-"),
         sg.Input(settings["LOC"]["altitude"], s=8, key="-ALT-"),],

        [sg.Text("Default settings:")],
        [sg.Text("Spacecraft ID:")],
        [sg.Input(settings["SCID"]["default_spacecraft"], s=22, key="-SCID-")],

        [sg.Text("Time step:")], 
        [sg.Input(settings["TIME"]["default_timestep"], s=4, key="-DTS-")],

        [sg.Text("Prediction span(H):")],
        [sg.Input(settings["TIME"]["default_timespan"], s=26, key="-TIMESPAN-")],

        [sg.Button("Save", key="-SAVE-", s=20)]

    ]

    #create settings window
    window = sg.Window("JEPT Settings", layout, modal=True)

    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED:
            break

        #settings
        if event == '-SAVE-':
            #write to ini file
            settings["LOC"]["latitude"] = values["-LAT-"]
            settings["LOC"]["laongitude"] = values["-LON-"]
            settings["LOC"]["altitude"] = values["-ALT-"]

            settings["SCID"]["default_spacecraft"] = values["-SCID-"]

            settings["TIME"]["default_timestep"] = values["-DTS-"]

            settings["TIME"]["default_timespan"] = values["-TIMESPAN-"]

            break
    window.close()



#Main window
def main_window():
    #Main LAYOUT
    layout = [

        [sg.Text("Spacecraft ID:")],
        [sg.Input(settings["SCID"]["default_spacecraft"], key="-SCID-", size=(14))],

        [sg.Text("From (YYYY-mm-dd HH-MM-SS):"), sg.Text("Time step:")],
        [sg.Input(timestart, key="-PSTART-", size=(26)), sg.Input(settings["TIME"]["default_timestep"], key="-STEP-", size=(10))],

        [sg.Text("To (YYYY-mm-dd HH-MM-SS):")],
        [sg.Input(timeend, key="-END-", size=(26))],

        [sg.Button("Run!", key="-START-"), sg.Button("Settings", key="-SET-")],

    ]

    #create main window
    window = sg.Window("JPL EPHEMRIS PROCESSING TOOL (J.E.P.T.)", layout)


    #create an even loop
    while True:
        event, values = window.read()

        #Execute GetAZEL if Start button pressed
        if event == '-START-':

            with open('temp.txt','w') as f: #Clears the temp.txt file
                    f.write("")
            #This code processes epheris data from JPL horizons
            #This code was written by Wyattaw and modified by mnux
            from astroquery.jplhorizons import Horizons
            import matplotlib.pyplot as plt
            import numpy as np
            # set your lat/long/elevation
            home = {'lat': int(settings["LOC"]["latitude"]), 'lon': int(settings["LOC"]["longitude"]), 'elevation': int(settings["LOC"]["altitude"])}
            # set minimum el to search above
            minEl = 0
            # create object to query horizons website
            obj = Horizons(id= values['-SCID-'],
                        location=home,
                        epochs={
                            'start': values['-PSTART-'],
                            'stop': values['-END-'],
                            'step': values['-STEP-']
                        })
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
                    print(T, A, E) #Terminal printout, T= UTC Time, A=Az, E=El,

                if E>= minEl:
                    with open('temp.txt','a') as f: #Writes the values to the tepm.txt file
                        f.write(T)
                        f.write(" ")
                        f.write(str(A))
                        f.write(" ")
                        f.write(str(E))
                        f.write("\n")

            # change az from deg to rad
            polarAzList = []
            for p in azList:
                polarAzList.append(np.deg2rad(p))

            # plot az el graph
            # need to find way to include time
            # plot
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

            plt.show()


        #Open settings if settings button is pressed
        if event == '-SET-':
            settings_window(settings)


        #end program if user closes window
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    SETTINGS_PATH = Path.cwd()
    #create setting object and use ini format
    settings = sg.UserSettings(
        path=SETTINGS_PATH, filename="config.ini", use_config_file=True, convert_bools_and_none=True
    )

theme = settings["GUI"]["theme"]
font_family = settings["GUI"]["font_family"]
font_size = int(settings["GUI"]["font_size"])

sg.theme(theme)
sg.set_options(font=(font_family, font_size))

main_window()