import PySimpleGUI as sg
from pathlib import Path


def main_window():
    #UI LAYOUT
    layout = [

        [sg.Text("Spacecraft ID:")],
        [sg.Input(key="-SCID-", size=(14,1))],

        [sg.Text("From (YYYY-mm-dd HH-MM-SS):"), sg.Text("Time step:")],
        [sg.Input(key="-FRM-", size=(26,1)), sg.Input(key="-STEP-", size=(10,1))],

        [sg.Text("To (YYYY-mm-dd HH-MM-SS):")],
        [sg.Input(key="-TO-", size=(26,1))],

        [sg.Button("START!", key="-START-")]
    ]



    #create window
    window = sg.Window("JPL EPHEMRIS PROCESSING TOOL (J.E.P.T.)", layout, )


    #create an even loop
    while True:
        event, values = window.read()

        #Execute GetAZEL if Start button pressed
        if event == '-START-':
            #This code processes epheris data from JPL horizons
            #This code was written by Wyattaw and modified by mnux
            from astroquery.jplhorizons import Horizons
            import matplotlib.pyplot as plt
            import numpy as np
            # set your lat/long/elevation
            home = {'lat': int(settings["LOC"]["latitude"]), 'lon': int(settings["LOC"]["longitude"]), 'elevation': int(settings["LOC"]["elevation"])}
            # set minimum el to search above
            minEl = 0
            # create object to query horizons website
            obj = Horizons(id= values['-SCID-'],
                        location=home,
                        epochs={
                            'start': values['-FRM-'],
                            'stop': values['-TO-'],
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