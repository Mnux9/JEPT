import PySimpleGUI as sg
from pathlib import Path
import datetime
from datetime import timedelta
import matplotlib.animation as animation
from astroquery.jplhorizons import Horizons
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import configparser

config = configparser.ConfigParser()

config.read('assets/config.ini')

timestart = datetime.datetime.now()
timestart = datetime.datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")


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
            settings["LOC"]["longitude"] = values["-LON-"]
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

        [sg.Text("Spacecraft ID:"),sg.Text("Time step:")],
        [sg.Input(settings["SCID"]["default_spacecraft"], key="-SCID-", size=(14)), sg.Input(settings["TIME"]["default_timestep"], key="-STEP-", size=(10))],

        [sg.Text("From (YYYY-mm-dd HH-MM-SS):")],
        [sg.Input(timestart, key="-PSTART-", size=(26))],

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

            settings["SCID"]["spacecraft"] = values["-SCID-"]

            #Clears the temp.txt file
            with open('temp.txt','w') as f:
                f.write("")


            #This code processes epheris data from JPL horizons
            #This code was written by Wyattaw and modified by mnux
            
            # set your lat/long/elevation
            home = {'lat': float(settings["LOC"]["latitude"]), 'lon': float(settings["LOC"]["longitude"]), 'elevation': float(settings["LOC"]["altitude"])}
            # set minimum el to search above
            minEl = 0
            # create object to query horizons website
            # prediction of the whole pass/es
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
                    print(T, A, E) #Terminal printout, T=Time, A=Az, E=El,

            # change az from deg to rad
            polarAzList = []
            for p in azList:
                polarAzList.append(np.deg2rad(p))


            # plot az el graph
            # need to find way to include time
            # plot
            fig = plt.figure(values['-SCID-'])
            ax = plt.subplot(121)
            ax.set_ylim(0, 90)
            ax.set_xlim(0, 360)
            ax.set_ylabel('Elevation')
            ax.set_xlabel('Azimuth')
            ax.set_xticks(np.arange(0, 360, 45))
            ax.grid(True)
            ax.plot(azList, elList)


            ax2 = plt.subplot(122, projection='polar')
            # make 90deg  in middle, 0deg on outside
            ax2.set_rlim(bottom=90, top=0)
            #rotate so 0deg AZ is on top
            ax2.set_theta_zero_location('N')
            # make theta increase clockwise
            ax2.set_theta_direction(-1)
            ax2.plot(polarAzList, elList)

            ax2 = plt.subplot(122, projection='polar')
            # make 90deg  in middle, 0deg on outside
            ax2.set_rlim(bottom=90, top=0)
            #rotate so 0deg AZ is on top
            ax2.set_theta_zero_location('N')
            # make theta increase clockwise
            ax2.set_theta_direction(-1)
            ax2.plot(polarAzList, elList)

            ax1 = plt.subplot(122, projection='polar')

            #Live polar plot
            def animate(i):

                #This code gets live position from JPL and writes it to file
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

                        with open('assets/temp.txt','w') as f: #Writes the values to the tepm.txt file                

                            f.write(str(A))
                            f.write(",")
                            f.write(str(E))
                            f.write("\n")




                graph_data = open('assets/temp.txt','r').read()
                lines = graph_data.split('\n')
                xs = []
                ys = []
                polarAzList = []

                ax1.clear()

                for line in lines:
                    if len(line) > 1:
                        x, y = line.split(',')
                        xs.append(float(x))
                        ys.append(float(y))
    
                for p in xs:
                    polarAzList.append(np.deg2rad(p))
                    
                

                # make 90deg  in middle, 0deg on outside
                ax1.set_rlim(bottom=90, top=0)
                #rotate so 0deg AZ is on top
                ax1.set_theta_zero_location('N')
                # make theta increase clockwise
                ax1.set_theta_direction(-1)

                ax1.scatter(polarAzList, ys)

            ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.show()


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
        path=SETTINGS_PATH, filename="assets/config.ini", use_config_file=True, convert_bools_and_none=True
    )

theme = settings["GUI"]["theme"]
font_family = settings["GUI"]["font_family"]
font_size = int(settings["GUI"]["font_size"])

sg.theme(theme)
sg.set_options(font=(font_family, font_size))

main_window()
