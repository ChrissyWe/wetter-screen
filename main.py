import tkinter as tk
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkvideo import tkvideo
import requests
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import time
import DriveManagement
import FileManagement
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import SensorInformation
import UTCI

def midnightProcedure():
    global currentTime
    global currentTemperature
    global currentHumidity
    global timesTodayFirst
    global timesTodaySecond
    global timesHumidityTodayFirst
    global timesHumidityTodaySecond
    global timesReferenceToday
    global temperaturesTodayFirst
    global temperaturesTodaySecond
    global temperatureReferenceToday
    global humidityTodaySecond
    global humidityToday
    global humidityReferenceToday
    global currentTimeTemp
    global currentTimeHumidity
    global currentTemperatureFirst
    global currentHumidityFirst
    global currentHumidityFirstSec
    global currentTimeTempSec
    global currentTimeHumiditySec
    global currentTemperatureFirstSec
    global currentTimes
    global humidityReferenceToday
    global temperatureReferenceToday

    currentTime = datetime.now()
    #DriveManagement.writeExcel()
    #FileManagement.create_csv(datetime.today().date())
    timesTodayFirst = [currentTimeTemp]
    timesTodaySecond = [currentTimeTempSec]
    timesHumidityTodayFirst = [currentTimeHumidity]
    timesHumidityTodaySecond = [currentTimeHumiditySec]
    timesReferenceToday = [currentTimes]

    temperaturesTodayFirst = [currentTemperatureFirst]
    temperaturesTodaySecond = [currentTemperatureFirstSec]
    temperatureReferenceToday = [currentTemperature]

    humidityToday = [currentHumidityFirst]
    humidityTodaySecond = [currentHumidityFirstSec]
    humidityReferenceToday = [currentHumidity]



    #read_file()

def updateDataSensor():
    currentTime = datetime.now()
    newTemperatureFifteen = SensorInformation.getTemperatureOutside()
    newTemperatureTwenty = SensorInformation.getTemperatureCorridor()
    #FileManagement.import_values_to_csv(newTime, newTemperatureFifteen, newTemperatureTwenty, minutesOverThirty)


def updateData():
    # Current Request
    global timesTodayFirst
    global temperaturesTodayFirst
    global humidityToday
    global times
    global humidity
    global temperatures
    global currentURL
    global currentData
    global currentTemperature
    global currentHumidity
    global utci
    global minutesOverThirty
    global currentTime
    global timesTodaySecond
    global timesHumidityTodayFirst
    global timesHumidityTodaySecond
    global timesReferenceToday
    global temperaturesTodaySecond
    global temperatureReferenceToday
    global humidityTodaySecond
    global humidityReferenceToday
    global currentTimeTemp
    global currentTimeHumidity
    global currentTemperatureFirst
    global currentHumidityFirst
    global currentTimeTempSec
    global currentTimeHumiditySec
    global currentTemperatureFirstSec
    global currentHumidityFirstSec
    global currentTimes
    global blocking

    blocking = True
    newTime = datetime.today()
    currentTime = datetime.now()
    #if newTemperatureOutside > 30:
     #   minutesOverThirty += 1
      #  updateFacts()


    #newTemperatureOutside = round(newTemperatureOutside, 1)
    #newTemperatureCorridor = round(newTemperatureCorridor, 1)

    currentData = requests.get(currentURL)

    if currentData.status_code == 200:
        currentJData = currentData.json()
    else:
        currentJData = "--"

    currentTemperature = float(currentJData["t2m_med"])
    currentHumidity = float(currentJData["rf_med"])
    currentTimes = dt.datetime.strptime(currentJData["measure_date"], date_format) + timedelta(hours=2)

    if (currentJData != "--") & (currentTimes != timesReference[len(timesReference) - 1]) & (currentTemperature < 50) & (currentHumidity <= 100):
        timesReference.pop(0)
        timesReference.append(currentTimes)
        timesReferenceToday.append(currentTimes)
        temperatureReference.pop(0)
        temperatureReference.append(currentTemperature)
        temperatureReferenceToday.append(currentTemperature)
        humidityReference.pop(0)
        humidityReference.append(currentHumidity)
        humidityReferenceToday.append(currentHumidity)

    windSensorFirstCurrent = requests.get(urlCurrentWind, headers=headers)
    windSensorSecondCurrent = requests.get(urlCurrentWindSecond, headers=headers)

    if windSensorFirstCurrent.status_code == 200:
        dataWindSensorFirstCurrent = windSensorFirstCurrent.json()
    else:
        dataWindSensorFirstCurrent = None
    if windSensorSecondCurrent.status_code == 200:
        dataWindSensorSecondCurrent = windSensorSecondCurrent.json()
    else:
        dataWindSensorSecondCurrent = None
    currentTimeTemp = 0
    currentTimeHumidity = 0
    currentTemperatureFirst = 0
    currentHumidityFirst = 0


    if dataWindSensorFirstCurrent is not None:
        for item in dataWindSensorFirstCurrent:
            if item["deviceId"] == '0004A30B00F7DA67':
                for time_series in item["timeSeries"]:
                    if time_series["timeSeriesId"] == '53787450-537a-451a-83f4-c8d62a8efacb':
                        currentTimeTemp = time_series["timestamps"][0]
                        currentTemperatureFirst = time_series["values"][0]
                    if time_series["timeSeriesId"] == 'e6c7a779-7b8b-4272-b42c-362ba7bf85b4':
                        currentTimeHumidity = time_series["timestamps"][0]
                        currentHumidityFirst = time_series["values"][0]

        currentTimeTemp = datetime.strptime(currentTimeTemp, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)
        currentTimeHumidity = datetime.strptime(currentTimeHumidity, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)

        if (times[len(times) - 1] < currentTimeTemp) & (currentTemperatureFirst < 50):
            times.pop(0)
            times.append(currentTimeTemp)
            temperatures.pop(0)
            temperatures.append(currentTemperatureFirst)
            timesTodayFirst.append(currentTimeTemp)
            temperaturesTodayFirst.append(currentTemperatureFirst)
        if (timesHumidity[len(timesHumidity) - 1] < currentTimeHumidity) & (currentHumidityFirst <= 100):
            timesHumidity.pop(0)
            timesHumidity.append(currentTimeHumidity)
            humidity.pop(0)
            humidity.append(currentHumidityFirst)
            timesHumidityTodayFirst.append(currentHumidityFirst)
            humidityToday.append(currentHumidityFirst)

    if dataWindSensorSecondCurrent is not None:
        for item in dataWindSensorSecondCurrent:
            if item["deviceId"] == '0004A30B00F7CD19':
                for time_series in item["timeSeries"]:
                    if time_series["timeSeriesId"] == '50bbdbe6-4136-4373-83cd-9bd50f451991':
                        currentTimeHumiditySec = time_series["timestamps"][0]
                        currentHumidityFirstSec = time_series["values"][0]
                    if time_series["timeSeriesId"] == 'f0e4473e-4ad5-40f5-b8f5-5d3768ea029a':
                        currentTimeTempSec = time_series["timestamps"][0]
                        currentTemperatureFirstSec = time_series["values"][0]

        currentTimeTempSec = datetime.strptime(currentTimeTempSec, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)
        currentTimeHumiditySec = datetime.strptime(currentTimeHumiditySec, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)

        if (timesSecond[len(timesSecond) - 1] < currentTimeTempSec) & (currentTemperatureFirstSec < 50):
            timesSecond.pop(0)
            timesSecond.append(currentTimeTempSec)
            temperaturesSecond.pop(0)
            temperaturesSecond.append(currentTemperatureFirstSec)
            timesTodaySecond.append(currentTimeTempSec)
            temperaturesTodaySecond.append(currentTemperatureFirstSec)
        if (timesHumiditySecond[len(timesHumiditySecond) - 1] < currentTimeHumiditySec) & (currentHumidityFirstSec <= 100):
            timesHumiditySecond.pop(0)
            timesHumiditySecond.append(currentTimeHumiditySec)
            humiditySecond.pop(0)
            humiditySecond.append(currentHumidityFirstSec)
            timesHumidityTodaySecond.append(currentTimeHumiditySec)
            humidityTodaySecond.append(currentHumidityFirstSec)

    #radiantTemperature = UTCI.calculateRadiantTemperature()
    #newUTCI = round(UTCI.universal_thermal_climate_index(float(currentData["t2m_med"]), float(currentData["t2m_med"]),
    #                                                  float(currentData["wg_med"]), float(currentData["rf_med"])), 1)
    newUTCI = "--"

    if (utci == None):
        utci = newUTCI
        updateUTCI()
    elif (utci != newUTCI):
        utci = newUTCI
        updateUTCI()

    now = datetime.now()
    if (datetime(now.year, now.month, now.day, 0, 10, 0) >= timesTodayFirst[len(timesTodayFirst) - 1] >= datetime(now.year, now.month, now.day, 0, 0, 0)):
        midnightProcedure()

    if currentTemperature > 30:
        minutesOverThirty += 1
        updateFacts()

    if (currentTime < (datetime.now() - timedelta(minutes=40))):
        currentTemperature = "--"
        utci = "--"

    print(currentTimeTempSec)
    print(currentTemperatureFirstSec)
    blocking = False

    root.after(600000, updateData)


def updateFacts():
    global informationTemperature
    global informationHumidity
    global currentTemperatureOutside
    global currentTemperatureCorridor
    global heatWithoutSystem
    global heatWithSystem
    global minutesOverThirty

    if informationHumidity is not None:
        informationHumidity.destroy()

    if informationTemperature is not None:
        informationTemperature.destroy()

    # Right Frame for Temperature Information
    informationTemperature = tk.Frame(informationGraphs)
    informationTemperature.pack(side="left", padx=10, pady=10)

    # Left Frame for Humidity Information
    informationHumidity = tk.Frame(informationGraphs)
    informationHumidity.pack(side="right", padx=10, pady=10)

    # Text above Graph
    current = f"Aktuelle Temperatur außen: {currentTemperature} °C"

    text_temperatures = tk.Text(informationTemperature, font=("Arial", 24), bg='white', fg='black', height=2,
                                width=50, borderwidth=0, highlightthickness=0)
    text_temperatures.pack(side="top")
    text_temperatures.insert("1.0", current)

    start_index = text_temperatures.search(str(currentTemperature) + " °C", "1.0", stopindex=tk.END)
    #second_occurrence_index = text_temperatures.search(str(currentTemperatureCorridor), f"{start_index}+1c", stopindex=tk.END)
    end_index = f"{start_index}+{len(str(currentTemperature)) + 3}c"
    text_temperatures.tag_configure("blue", foreground="blue", font=("Arial", 24, "bold"))
    text_temperatures.tag_add("blue", start_index, end_index)

    text_temperatures.tag_configure("blue", foreground="blue", font=("Arial", 24, "bold"))
    #text_temperatures.tag_add("blue", second_occurrence_index,
                            #  f"{second_occurrence_index}+{len(str(currentTemperatureCorridor)) + 3}c")

    heatWithSystem = "0 h"
    heatWithoutSystem = str(int(minutesOverThirty / 6)) + " h"

    # Text beside Humidity
    humidity_information = f"Stunden über 30°C seit Messung außen, ohne Sprühanlage: {heatWithoutSystem}"

    text_humidity_information = tk.Text(informationHumidity, font=("Arial", 24), bg='white', fg='black', height=2,
                                        width=50, borderwidth=0, highlightthickness=0)
    text_humidity_information.pack(side="top")
    text_humidity_information.insert("1.0", humidity_information)

    startIndexHumidity = text_humidity_information.search(str(heatWithoutSystem), "1.0", stopindex=tk.END)
    #secondIndexHumidity = text_humidity_information.search(str(heatWithSystem), f"{startIndexHumidity}+1c",
                                                         #  stopindex=tk.END)
    endIndexHumidity = f"{startIndexHumidity}+{len(str(heatWithoutSystem))}c"
    #secondEndHumidity = f"{secondIndexHumidity}+{len(str(heatWithSystem))}c"
    text_humidity_information.tag_configure("blue", foreground="blue", font=("Arial", 24, "bold"))
    #text_humidity_information.tag_add("blue", secondIndexHumidity, secondEndHumidity)
    text_humidity_information.tag_add("blue", startIndexHumidity, endIndexHumidity)


def updateUTCI():
    global utci
    global UTCIImage
    global UTCIArrow
    global textUTCI
    global arrow
    global canvas
    global UTCIFrame
    global UTCIBuffer

    if textUTCI is not None:
        UTCIFrame.destroy()

    if UTCIBuffer is not None:
        UTCIBuffer.destroy()

    # UTCI Calculator
    UTCIFrame = tk.Frame(rightFrame, bg="#F0F8FF")
    UTCIFrame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    # UTCI Information
    UTCIBuffer = tk.Frame(UTCIFrame, bg="#F0F8FF")
    UTCIBuffer.pack(side="top", fill="both", expand=True, pady=130)
    currentUTCI = f"Gefühlte Außenluft-\nTemperatur Aktuell: \n {utci} °C"

    textUTCI = tk.Text(UTCIBuffer, font=("Arial", 24), bg='#F0F8FF', fg='black', height=3, width=20, borderwidth=0, highlightthickness=0)
    textUTCI.insert("1.0", currentUTCI, "center")
    textUTCI.tag_configure("center", justify="center")
    textUTCI.pack(side="top")

    # Makes the Temperature blue
    startIndexUTCI = textUTCI.search(str(utci) + " °C", "1.0", stopindex=tk.END)
    endIndexUTCI = f"{startIndexUTCI}+{len(str(utci)) + 3}c"
    textUTCI.tag_configure("blue", foreground="blue", font=("Arial", 24, "bold"))
    textUTCI.tag_add("blue", startIndexUTCI, endIndexUTCI)

    # Canvas, width normally 264
    canvas = tk.Canvas(UTCIBuffer, width=int((264) + 10 + 45), height=int((1753) + 20), bg='#F0F8FF', highlightthickness=0)
    canvas.pack(side="top")

    UTCIImage = tk.PhotoImage(file=r"C:\Users\Chris\PycharmProjects\pythonProject\pictures\UTCI-Chart.png")
    #UTCIImage = tk.PhotoImage(file="/home/buga/wetter-screen/pictures/UTCI-Chart.png")
    #UTCIImage = UTCIImage.subsample(2)  # Resize 1/2
    canvas.create_image(45, 10, anchor="nw", image=UTCIImage)

    # Draw Arrow with Text
    UTCIArrow = tk.PhotoImage(file=r"C:\Users\Chris\PycharmProjects\pythonProject\pictures\UTCI-Arrow.png")
    #UTCIArrow = tk.PhotoImage(file="/home/buga/wetter-screen/pictures/UTCI-Arrow.png")
    #UTCIArrow = UTCIArrow.subsample(2)
    if utci == "--":
        utci = ""
    elif utci <= -13:
        arrow = canvas.create_image(-5, 815, anchor="nw", image=UTCIArrow)
    elif utci <= 0:
        koordinate = 815 - ((utci + 13) * (18.5/2))
        arrow = canvas.create_image(-5, koordinate, anchor="nw", image=UTCIArrow)
    elif utci <= 9:
        koordinate = 694.75 - ((utci) * (120/9))
        arrow = canvas.create_image(-5, koordinate, anchor="nw", image=UTCIArrow)
    elif utci <= 26:
        koordinate = 574.5 - ((utci - 9) * (120/17))
        arrow = canvas.create_image(-5, koordinate, anchor="nw", image=UTCIArrow)
    elif utci <= 32:
        koordinate = 454.5 - ((utci - 26) * (120/6))
        arrow = canvas.create_image(-5, koordinate, anchor="nw", image=UTCIArrow)
    elif utci <= 38:
        koordinate = 214.5 - ((utci - 38) * (120/6))
        arrow = canvas.create_image(-5, koordinate, anchor="nw", image=UTCIArrow)

    # UTCI = Universal Thermal Climate Index
    currentUTCI = f"(UTCI - Universal \nThermal Climate Index)"

    textUTCI = tk.Text(UTCIBuffer, font=("Arial", 14), bg='#F0F8FF', fg='black', height=3, width=20, borderwidth=0, highlightthickness=0)
    textUTCI.insert("1.0", currentUTCI, "center")
    textUTCI.tag_configure("center", justify="center")
    textUTCI.tag_add("center", "1.0", "end")
    textUTCI.pack(side="top")


def toggleGraphs():
    global currentGraphTemperature
    global currentGraphHumidity
    global counter
    global axTemperature
    global axHumidity
    global figTemperature
    global figHumidity

    if blocking:
        time.sleep(10)
    if currentGraphTemperature is not None:
        axTemperature.clear()
        plt.close(figTemperature)
        currentGraphTemperature.get_tk_widget().destroy()

    if currentGraphHumidity is not None:
        axHumidity.clear()
        plt.close(figHumidity)
        currentGraphHumidity.get_tk_widget().destroy()

    if counter == 0:
        figureTemperature, axTemperature, figTemperature = createTemperatureGraphWeek()
        currentGraphTemperature = figureTemperature
        figureHumidity, axHumidity, figHumidity = createHumidityGraphWeek()
        currentGraphHumidity = figureHumidity
        counter = 1
    else:
        figureTemperature, axTemperature, figTemperature = createTemperatureGraphDay()
        currentGraphTemperature = figureTemperature
        figureHumidity, axHumidity, figHumidity = createHumidityGraphDay()
        currentGraphHumidity = figureHumidity
        counter = 0

    currentGraphTemperature.get_tk_widget().pack(side="top", fill="both", expand=True)

    currentGraphHumidity.get_tk_widget().pack(side="top", fill="both", expand=True)

    root.after(15000, toggleGraphs)


def createTemperatureGraphWeek():
    # Graph 1 (Temperature - Week)
    fig1, ax1 = plt.subplots()
    ax1.set_title('Temperaturen letzte Woche', color="black", fontsize=28)
    ax1.set_ylabel("Temperatur", fontsize=16)
    ax1.set_xlabel("Datum", fontsize=16)
    #ax1.set_xlim(times[len(times) - 1], currentTime)
    ax1.tick_params(colors="black")
    for spine in ax1.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax1.fill_between((datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0), currentTime), 0,
                     40, facecolor='orange', alpha=0.2)
    #ax1.fill_between(times_second, temperatures_second, color="#f8686a", alpha=0.1)
    ax1.set_frame_on(False)
    ax1.plot(times, temperatures, color="firebrick", label="Temperatur Außen", linewidth=2.5)
    ax1.plot(timesSecond, temperaturesSecond, color="#f8686a", label="Temperatur Korridor", linestyle="--", linewidth=2.5)
    ax1.plot(timesReference, temperatureReference, color="black", label="Referenz", linewidth=1)
    legend = ax1.legend(fontsize=16)
    legend.get_frame().set_facecolor("#F0F8FF")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    #fig1.patch.set_facecolor('#F0F8FF')
    #ax1.set_facecolor('#F0F8FF')
    figure = FigureCanvasTkAgg(fig1, master=graph_frame)
    return figure, ax1, fig1


def createTemperatureGraphDay():
    # Graph 1 (Temperature - Day)
    fig3, ax3 = plt.subplots()
    ax3.set_title('Temperaturen heute', color="black", fontsize=28)
    ax3.set_ylabel("Temperatur", fontsize=16)
    ax3.set_xlabel("Uhrzeit", fontsize=16)
    #ax3.set_xlim(times_today_first[0], currentTime)
    ax3.tick_params(colors="black")
    for spine in ax3.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax3.fill_between((datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0), currentTime), 0,
                     40, facecolor='orange', alpha=0.2)
    ax3.fill_between(timesTodaySecond, temperaturesTodaySecond, color="#f8686a", alpha=0.1)
    ax3.set_frame_on(False)
    ax3.plot(timesTodayFirst, temperaturesTodayFirst, color="firebrick", label="Temperatur Außen", linewidth=2.5)
    ax3.plot(timesTodaySecond, temperaturesTodaySecond, color="#f8686a", label="Temperatur Korridor", linestyle="--", linewidth=2.5)
    ax3.plot(timesReferenceToday, temperatureReferenceToday, color="black", label="Referenz", linewidth=1)
    legend = ax3.legend(fontsize=16)
    legend.get_frame().set_facecolor("#F0F8FF")
    #fig3.patch.set_facecolor('#F0F8FF')
    figure = FigureCanvasTkAgg(fig3, master=graph_frame)
    return figure, ax3, fig3


def createHumidityGraphWeek():
    # Graph 2 (Humidity)
    fig2, ax2 = plt.subplots()
    ax2.set_title('Relative Luftfeuchte letzte Woche', color="black", fontsize=28)
    ax2.set_ylabel("Luftfeuchte", color="black", fontsize=16)
    ax2.set_xlabel("Datum", fontsize=16)
    ax2.tick_params(colors="black")
    for spine in ax2.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax2.fill_between((datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0), currentTime), 0,
                     100, facecolor='orange', alpha=0.2)
    ax2.fill_between(timesSecond, humiditySecond, color="teal", alpha=0.1)
    ax2.set_frame_on(False)
    ax2.plot(times, humidity, label="Luftfeuchte Außen", linewidth=2.5)
    ax2.plot(timesSecond, humiditySecond, color="teal", label="Luftfeuchte Korridor", linestyle="--", linewidth=2.5)
    ax2.plot(timesReference, humidityReference, color="black", label="Referenz", linewidth=1)
    legend = ax2.legend(fontsize=16)
    legend.get_frame().set_facecolor("#F0F8FF")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    #fig2.patch.set_facecolor('#F0F8FF')
    #ax2.set_facecolor('#F0F8FF')
    figure = FigureCanvasTkAgg(fig2, master=graph_frame)
    return figure, ax2, fig2


def createHumidityGraphDay():
    fig4, ax4 = plt.subplots()
    ax4.set_title('Relative Luftfeuchte heute', color="black", fontsize=28)
    ax4.set_ylabel("Luftfeuchte", color="black", fontsize=16)
    ax4.tick_params(colors="black")
    for spine in ax4.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax4.fill_between(
            (datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0), currentTime), 0,
            100, facecolor='orange', alpha=0.2)
    #ax4.fill_between(times_today_second, humidity_today_second, color="teal", alpha=0.1)
    ax4.set_frame_on(False)
    ax4.plot(timesTodayFirst, humidityToday, label="Luftfeuchte Aussen", linewidth=2.5)
    ax4.plot(timesTodaySecond, humidityTodaySecond, color="teal", label="Luftfeuchte Korridor", linestyle="--", linewidth=2.5)
    ax4.plot(timesReferenceToday, humidityReferenceToday, color="black", label="Referenz", linewidth=1)
    legend = ax4.legend(fontsize=16)
    legend.get_frame().set_facecolor("#F0F8FF")
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    #fig4.patch.set_facecolor('#F0F8FF')
    #ax4.set_facecolor('#F0F8FF')
    figure = FigureCanvasTkAgg(fig4, master=graph_frame)
    return figure, ax4, fig4


def read_file():
    generalInformation = "TODO"
    #textInformation.delete("1.0", tk.END)
    #textInformation.insert(tk.END, generalInformation)
    #textInformation.tag_configure("left_align", justify="left")
    #textInformation.tag_add("left_align", "1.0", tk.END)



#----------- Get Information -----------#

# Date Information
today_date = datetime.today()
date_last_week = today_date + timedelta(days=-7)
todayMidnight = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)
date_format = '%Y-%m-%dT%H:%M:%SZ'

print(today_date)
print(today_date.strftime('%Y-%m-%d'))
print(date_last_week.strftime('%Y-%m-%d'))

blocking = False

# Current Request
#urlCurrent = "https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/current/288"
#dataCurrent = requests.get(urlCurrent).json()

# Data Request Station 288
stationURL = f"https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/historic/288/{date_last_week.strftime('%Y-%m-%d')}/{today_date.strftime('%Y-%m-%d')}"
currentURL = "https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/current/288"
data = requests.get(stationURL)

if data.status_code == 200:
    stationData = data.json()

# data reference station
timesReference = [dt.datetime.strptime(element, date_format) + timedelta(hours=2) for element in stationData["data"]]
timesReferenceToday = list(filter(lambda x: x >= todayMidnight, timesReference))
temperatureReference = [float(stationData["data"][element]["t2m_med"]) for element in stationData["data"]]
temperatureReferenceToday = temperatureReference[:len(timesReferenceToday)]
humidityReference = [float(stationData["data"][element]["rf_med"]) for element in stationData["data"]]
humidityReferenceToday = humidityReference[:len(timesReferenceToday)]



# Data Request Station 287
#urlSecond = f"https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/historic/287/{date_last_week.strftime('%Y-%m-%d')}/{today_date.strftime('%Y-%m-%d')}"
#dataSecond = requests.get(url).json()

# Data Request
subscriptionKey = 'd99c1e9e7d2e4acab55672df0bfc50ce'

headers = {
    'accept': 'application/json',
    'Ocp-Apim-Subscription-Key': subscriptionKey
}

# Devices (Temperature?)
urlWindSensor1 = "https://api.mvvsmartcities.com/v3/device/timeseries?deviceId=0004A30B00F7DA67&sort=desc&limit=1140&output=split&metadata=false"
urlWindSensor2 = "https://api.mvvsmartcities.com/v3/device/timeseries?deviceId=0004A30B00F7CD19&sort=desc&limit=1140&output=split&metadata=false"
urlCurrentWind = "https://api.mvvsmartcities.com/v3/device/timeseries?deviceId=0004A30B00F7DA67&sort=desc&limit=1&output=split&metadata=false"
urlCurrentWindSecond = "https://api.mvvsmartcities.com/v3/device/timeseries?deviceId=0004A30B00F7CD19&sort=desc&limit=1&output=split&metadata=false"

# Devices (Air?)
urlAirSensor1 = "https://api.mvvsmartcities.com/v3/device/timeseries?deviceId=0004A30B0103B729&sort=desc&limit=1140&output=split&metadata=false"
urlAirSensor2 = "https://api.mvvsmartcities.com/v3/device/timeseries?deviceId=0004A30B0103EBED&sort=desc&limit=1140&output=split&metadata=false"
urlCurrentAir = "https://api.mvvsmartcities.com/v3/device/timeseries?deviceId=0004A30B0103B729&sort=desc&limit=1&output=split&metadata=false"
urlCurrentAirSecond = "https://api.mvvsmartcities.com/v3/device/timeseries?deviceId=0004A30B0103EBED&sort=desc&limit=1&output=split&metadata=false"

utci = None

windSensorFirstWeek = requests.get(urlWindSensor1, headers=headers)
windSensorSecondWeek = requests.get(urlWindSensor2, headers=headers)
airSensorFirstWeek = requests.get(urlAirSensor1, headers=headers)
airSensorSecondWeek = requests.get(urlAirSensor2, headers=headers)

if windSensorFirstWeek.status_code == 200:
    dataWindSensorFirstWeek = windSensorFirstWeek.json()
if windSensorSecondWeek.status_code == 200:
    dataWindSensorSecondWeek = windSensorSecondWeek.json()
if airSensorFirstWeek.status_code == 200:
    dataAirSensorFirstWeek = airSensorFirstWeek.json()
if airSensorSecondWeek.status_code == 200:
    dataAirSensorSecondWeek = airSensorSecondWeek.json()

# Values of Temperatures
# Today
timesTodayFirst = []
timesTodaySecond = []
timesHumidityTodayFirst = []
timesHumidityTodaySecond = []
temperaturesTodayFirst = []
temperaturesTodaySecond = []
humidityToday = []
humidityTodaySecond = []

# Week
times = []
timesHumidity = []
timesSecond = []
timesHumiditySecond = []
humidity = []
humiditySecond = []
temperatures = []
temperaturesSecond = []
minutesOverThirty = 0

for item in dataWindSensorFirstWeek:
    if item["deviceId"] == '0004A30B00F7DA67':
        for time_series in item["timeSeries"]:
            if time_series["timeSeriesId"] == '53787450-537a-451a-83f4-c8d62a8efacb':
                times = time_series["timestamps"]
                temperatures = time_series["values"]
            if time_series["timeSeriesId"] == 'e6c7a779-7b8b-4272-b42c-362ba7bf85b4':
                timesHumidity = time_series["timestamps"]
                humidity = time_series["values"]

times = list(map(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"), times))
times = list(map(lambda x: x + timedelta(hours=2), times))
times = list(filter(lambda x: x > (date_last_week + timedelta(days=-1)), times))
temperatures = temperatures[:len(times)]
timesHumidity = list(map(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"), timesHumidity))
timesHumidity = list(map(lambda x: x + timedelta(hours=2), timesHumidity))
timesHumidity = list(filter(lambda x: x > (date_last_week + timedelta(days=-1)), timesHumidity))
humidity = humidity[:len(timesHumidity)]

timesTodayFirst = list(filter(lambda x: x >= todayMidnight, times))
temperaturesTodayFirst = temperatures[:len(timesTodayFirst)]
timesHumidityTodayFirst = list(filter(lambda x: x >= todayMidnight, timesHumidity))
humidityToday = humidity[:len(timesHumidityTodayFirst)]

times = times[::-1]
timesHumidity = timesHumidity[::-1]
timesTodayFirst = timesTodayFirst[::-1]
temperaturesTodayFirst = temperaturesTodayFirst[::-1]
timesHumidityTodayFirst = timesHumidityTodayFirst[::-1]
humidityToday = humidityToday[::-1]

for item in dataWindSensorSecondWeek:
    if item["deviceId"] == '0004A30B00F7CD19':
        for time_series in item["timeSeries"]:
            if time_series["timeSeriesId"] == '50bbdbe6-4136-4373-83cd-9bd50f451991':
                timesHumiditySecond = time_series["timestamps"]
                humiditySecond = time_series["values"]
            if time_series["timeSeriesId"] == 'f0e4473e-4ad5-40f5-b8f5-5d3768ea029a':
                timesSecond = time_series["timestamps"]
                temperaturesSecond = time_series["values"]

timesHumiditySecond = list(map(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"), timesHumiditySecond))
timesHumiditySecond = list(map(lambda x: x + timedelta(hours=2), timesHumiditySecond))
timesHumiditySecond = list(filter(lambda x: x > (date_last_week + timedelta(days=-1)), timesHumiditySecond))
humiditySecond = humiditySecond[:len(timesHumiditySecond)]
timesSecond = list(map(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"), timesSecond))
timesSecond = list(map(lambda x: x + timedelta(hours=2), timesSecond))
timesSecond = list(filter(lambda x: x > (date_last_week + timedelta(days=-1)), timesSecond))
temperaturesSecond = temperaturesSecond[:len(timesSecond)]

timesTodaySecond = list(filter(lambda x: x >= todayMidnight, timesSecond))
temperaturesTodaySecond = temperaturesSecond[:len(timesTodaySecond)]
timesHumidityTodaySecond = list(filter(lambda x: x >= todayMidnight, timesHumiditySecond))
humidityTodaySecond = humiditySecond[:len(timesHumidityTodaySecond)]

currentTemperature = temperatures[0]
currentTime = times[0]
print(currentTemperature)

timesHumiditySecond = timesHumiditySecond[::-1]
timesSecond = timesSecond[::-1]
timesTodaySecond = timesTodaySecond[::-1]
temperaturesTodaySecond = temperaturesTodaySecond[::-1]
timesHumidityTodaySecond = timesHumidityTodaySecond[::-1]
humidityTodaySecond = humidityTodaySecond[::-1]

#----------- Create Important Information -----------#

# Create First File
###########################FileManagement.create_csv(datetime.today().date())

# Main-Window
root = tk.Tk()
root.config(background="white")
#root.attributes("-fullscreen", True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#4096, 2160
root.geometry(f"{screen_width}x{screen_height}")
left_width_pct = 0.5
right_width_pct = 1.0 - left_width_pct

# Get Font
font_family = "Ubuntu Bold"
font_size = 48
custom_font = font.Font(family=font_family, size=font_size)


#----------- Frame Management -----------#

#--- Left Frame ---#
text_frame = tk.Frame(root, bg="white")
text_frame.pack(side="left", fill="both", expand=True)

# Frame MP4
#videoFrame = tk.Frame(text_frame, bg="#F0F8FF")
#videoFrame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# Header "Visualisierungen zu Planung und Fertigung"
#header_visualization = tk.Label(videoFrame, text='Visualisierungen zu Planung und Fertigung', justify="left", font=custom_font, bg='#F0F8FF', fg='black')
#header_visualization.pack(side="top", padx=10, pady=10)

# Video
#my_label = tk.Label(videoFrame, justify="left")
#my_label.pack()

#player = tkvideo(r"C:\Users\Chris\PycharmProjects\pythonProject\pictures\sample.mp4", my_label, loop=1, size=(1280, 720))
#player = tkvideo("/home/buga/wetter-screen/pictures/sample.mp4", my_label, loop=1, size=(1280, 720))
#player.play()

# Frame Information
informationFrame = tk.Frame(text_frame, bg="#F0F8FF")
informationFrame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

#--- Right Frame ---#
rightFrame = tk.Frame(root, bg="white")
rightFrame.pack(side="right", fill="both", expand=True)

#- Right-Left Frame -#
graph_frame = tk.Frame(rightFrame, bg="white")
graph_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Value Format
date_format = '%Y-%m-%dT%H:%M:%SZ'

currentTime = datetime.today()
#currentTemperatureFifteen = SensorInformation.getTemperatureOutside()
#currentTemperatureTwenty = SensorInformation.getTemperatureCorridor()



delta = timedelta(hours=2)

# for element in data["data"]:
###################     rightTime = datetime.strptime(str(element), date_format) + delta
#     times.append(rightTime)
#     temperatures.append(float(data["data"][element]["t2m_med"]))
#     if (float(data["data"][element]["t2m_med"]) > 30):
#         minutesOverThirty += 1
#     if rightTime >= (datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)):
#         times_today_first.append(rightTime)
#         temperatures_today_first.append(float(data["data"][element]["t2m_med"]))
#         humidityToday.append(float(data["data"][element]["rf_med"]))
#     humidity.append(float(data["data"][element]["rf_med"]))

if(currentTime < (datetime.now() - timedelta(minutes=40))):
    currentTemperature = "--"
    utci = "--"


# Header "Informationen zum Mikroklima dieses Pavillions"
header_climate = tk.Label(graph_frame, text='Informationen zum Mikroklima dieses Pavillons', font=custom_font, bg='white', fg='black', anchor="w")
header_climate.pack(side="top", padx=10, pady=10)

#Frame for Information
informationGraphs = tk.Frame(graph_frame, bg='white')
informationGraphs.pack(side="top")

informationHumidity = None
informationTemperature = None
updateFacts()


counter = 0
temperatureGraphDay = createTemperatureGraphDay()
temperatureGraphWeek = createTemperatureGraphWeek()
humidityGraphDay = createHumidityGraphDay()
humidityGraphWeek = createHumidityGraphWeek()

currentGraphHumidity = None
currentGraphTemperature = None
ax1 = None
ax2 = None
ax3 = None
ax4 = None
toggleGraphs()

UTCIFrame = None
UTCIBuffer = None
textUTCI = None
UTCIImage = None
UTCIArrow = None
updateData()

# Main loop
root.mainloop()
