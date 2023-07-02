import tkinter as tk
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkvideo import tkvideo
from tkVideoPlayer import TkinterVideo
import requests
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import DriveManagement
import FileManagement
#import pyglet
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import SensorInformation
import UTCI

def midnightProcedure():
    global currentTime
    global times_today_first
    global times_today_second
    global temperatures_today_first
    global temperatures_today_second
    currentTime = datetime.now()
    #DriveManagement.writeExcel()
    FileManagement.create_csv(datetime.today().date())
    times_today_first = [currentTime]
    times_today_second = [currentTime]
    temperatures_today_first = [SensorInformation.getTemperatureOutside()]
    temperatures_today_second = [SensorInformation.getTemperatureOutside()]
    #read_file()


def updateData():
    # Current Request
    global times_today_first
    global temperatures_today_first
    global humidityToday
    global times
    global timesMatplotlib
    global humidity
    global temperatures
    global currentURL
   # global currentData
    global utci
    global minutesOverThirty
    global currentTemperatureOutside
    global currentTemperatureCorridor
    global currentTime

    newTime = datetime.today()
    currentTime = datetime.now()
    newTemperatureOutside = SensorInformation.getTemperatureOutside()
    newTemperatureCorridor = SensorInformation.getTemperatureCorridor()
    if newTemperatureOutside > 30:
        minutesOverThirty += 1
        updateFacts()

    FileManagement.import_values_to_csv(newTime, newTemperatureOutside, newTemperatureCorridor, minutesOverThirty)

    newTemperatureOutside = round(newTemperatureOutside, 1)
    newTemperatureCorridor = round(newTemperatureCorridor, 1)

    currentURL = "https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/current/288"
    currentData = requests.get(currentURL).json()

    newUTCI = round(UTCI.universal_thermal_climate_index(float(currentData["t2m_med"]), float(currentData["t2m_med"]),
                                                      float(currentData["wg_med"]), float(currentData["rf_med"])), 1)


    if (utci == None):
        utci = newUTCI
        updateUTCI()
    elif (utci != newUTCI):
        utci = newUTCI
        updateUTCI()

    now = datetime.now()
    if (datetime(now.year, now.month, now.day, 0, 5, 0) >= times_today_first[len(times_today_first) - 1] >= datetime(now.year, now.month, now.day, 0, 0, 0)):
        midnightProcedure()
        #humidityToday = []

    if(times[0] <= (datetime.now() - timedelta(days=7))):
        times.pop(0)
        times_second.pop(0)
        temperatures.pop(0)
        temperatures_second.pop(0)
    times.append(newTime)
    times_second.append(newTime)
    times_today_first.append(newTime)
    times_today_second.append(newTime)
    temperatures.append(newTemperatureOutside)
    temperatures_second.append(newTemperatureCorridor)
    temperatures_today_first.append(newTemperatureOutside)
    temperatures_today_second.append(newTemperatureCorridor)
    if newTemperatureOutside > 30:
        minutesOverThirty += 1
        updateFacts()
    if currentTemperatureOutside != newTemperatureOutside:
        currentTemperatureOutside = newTemperatureOutside
        updateFacts()
    if currentTemperatureCorridor != newTemperatureCorridor:
        currentTemperatureCorridor = newTemperatureCorridor
        updateFacts()

    #if((datetime.strptime(str(currentData["measure_date"]), date_format)) + delta != times[len(times) - 1]):
    #    times.pop(0)
    #    times.append(datetime.strptime(str(currentData["measure_date"]), date_format) + delta)
    #    times_today_first.append(datetime.strptime(str(currentData["measure_date"]), date_format) + delta)
    #    humidity.pop(0)
    #    humidity.append(float(currentData["rf_med"]))
    #    humidityToday.append(float(currentData["rf_med"]))
    #    temperatures.pop(0)
    #    newTemperature = float(currentData["t2m_med"])
    #    if newTemperature > 30:
    #        minutesOverThirty += 1
    #        updateFacts()
    #    temperatures.append(newTemperature)
    #    temperatures_today_first.append(newTemperature)
    #    print(datetime.strptime(str(currentData["measure_date"]), date_format) + delta)
    #    if (currentTemperature != newTemperature):
    #        currentTemperature = newTemperature
    #        updateFacts()


    root.after(300000, updateData)


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
    current = f"Aktuelle Temperatur außen: {currentTemperatureOutside} °C\nAktuelle Temperatur in Sprühanlage: {currentTemperatureCorridor} °C"

    text_temperatures = tk.Text(informationTemperature, font=("Arial", 24), bg='white', fg='black', height=2,
                                width=50, borderwidth=0, highlightthickness=0)
    text_temperatures.pack(side="top")
    text_temperatures.insert("1.0", current)

    start_index = text_temperatures.search(str(currentTemperatureOutside) + " °C", "1.0", stopindex=tk.END)
    second_occurrence_index = text_temperatures.search(str(currentTemperatureCorridor), f"{start_index}+1c", stopindex=tk.END)
    end_index = f"{start_index}+{len(str(currentTemperatureCorridor)) + 3}c"
    text_temperatures.tag_configure("blue", foreground="blue", font=("Arial", 24, "bold"))
    text_temperatures.tag_add("blue", start_index, end_index)

    text_temperatures.tag_configure("blue", foreground="blue", font=("Arial", 24, "bold"))
    text_temperatures.tag_add("blue", second_occurrence_index,
                              f"{second_occurrence_index}+{len(str(currentTemperatureCorridor)) + 3}c")

    heatWithSystem = "0 h"
    heatWithoutSystem = str(int(minutesOverThirty / 6)) + " h"

    # Text beside Humidity
    humidity_information = f"Stunden über 30°C bis jetzt außen, ohne Sprühanlage: {heatWithoutSystem}\nStunden über 30°C bis jetzt mit Sprühanlage: {heatWithSystem}"

    text_humidity_information = tk.Text(informationHumidity, font=("Arial", 24), bg='white', fg='black', height=2,
                                        width=50, borderwidth=0, highlightthickness=0)
    text_humidity_information.pack(side="top")
    text_humidity_information.insert("1.0", humidity_information)

    startIndexHumidity = text_humidity_information.search(str(heatWithoutSystem), "1.0", stopindex=tk.END)
    secondIndexHumidity = text_humidity_information.search(str(heatWithSystem), f"{startIndexHumidity}+1c",
                                                           stopindex=tk.END)
    endIndexHumidity = f"{startIndexHumidity}+{len(str(heatWithoutSystem))}c"
    secondEndHumidity = f"{secondIndexHumidity}+{len(str(heatWithSystem))}c"
    text_humidity_information.tag_configure("blue", foreground="blue", font=("Arial", 24, "bold"))
    text_humidity_information.tag_add("blue", secondIndexHumidity, secondEndHumidity)
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

    UTCIImage = tk.PhotoImage(file="/home/buga/wetter-screen/pictures/UTCI-Chart.png")
    #UTCIImage = UTCIImage.subsample(2)  # Resize 1/2
    canvas.create_image(45, 10, anchor="nw", image=UTCIImage)

    # Draw Arrow with Text
    UTCIArrow = tk.PhotoImage(file="/home/buga/wetter-screen/pictures/UTCI-Arrow.png")
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

    if currentGraphTemperature is not None:
        axTemperature.clear()
        plt.close(figTemperature)
        currentGraphTemperature.get_tk_widget().destroy()

    #if currentGraphHumidity is not None:
    #    axHumidity.clear()
    #    plt.close(figHumidity)
    #    currentGraphHumidity.get_tk_widget().destroy()

    if counter == 0:
        figureTemperature, axTemperature, figTemperature = createTemperatureGraphWeek()
        currentGraphTemperature = figureTemperature
        #figureHumidity, axHumidity, figHumidity = createHumidityGraphWeek()
        #currentGraphHumidity = figureHumidity
        counter = 1
    else:
        figureTemperature, axTemperature, figTemperature = createTemperatureGraphDay()
        currentGraphTemperature = figureTemperature
        #figureHumidity, axHumidity, figHumidity = createHumidityGraphDay()
        #currentGraphHumidity = figureHumidity
        counter = 0

    #graphFrameTemperature = tk.Frame(informationGraphs, bg="green")
    #graphFrameTemperature.pack(side="top", fill="both", expand=True)
    currentGraphTemperature.get_tk_widget().pack(side="top", fill="both", expand=True)

    #graphFrameHumidity = tk.Frame(informationGraphs, bg="green")
    #graphFrameHumidity.pack(side="top", fill="both", expand=True)
    #currentGraphHumidity.get_tk_widget().pack(side="top", fill="both", expand=True)

    root.after(15000, toggleGraphs)


def createTemperatureGraphWeek():
    # Graph 1 (Temperature - Week)
    fig1, ax1 = plt.subplots()
    ax1.set_title('Temperaturen letzte Woche', color="black", fontsize=28)
    #fig1.suptitle("letzte Woche", fontsize=28, fontweight='bold', y=1)
    #fig1.text(0.5, 0.97, "Temperaturen", fontsize=32, fontweight='bold', ha='center')
    #fig1.text(0.5, 0.97, "diese Woche", fontsize=32, fontweight='bold', ha='right')
    ax1.set_ylabel("Temperatur", fontsize=16)
    ax1.set_xlabel("Datum", fontsize=16)
    ax1.set_xlim(times[0], currentTime)
    ax1.tick_params(colors="black")
    for spine in ax1.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax1.fill_between((datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0), currentTime), 0,
                     40, facecolor='orange', alpha=0.2)
    ax1.fill_between(times_second, temperatures_second, color="#f8686a", alpha=0.1)
    ax1.set_frame_on(False)
    ax1.plot(times, temperatures, color="firebrick", label="Temperatur Außen", linewidth=2.5)
    ax1.plot(times_second, temperatures_second, color="#f8686a", label="Temperatur Korridor", linestyle="--", linewidth=2.5)
    legend = ax1.legend(fontsize=16)
    legend.get_frame().set_facecolor("#F0F8FF")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.,%H:%M'))
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
    ax3.set_xlim(times_today_first[0], currentTime)
    ax3.tick_params(colors="black")
    for spine in ax3.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax3.fill_between((datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0), currentTime), 0,
                     40, facecolor='orange', alpha=0.2)
    ax3.fill_between(times_today_second, temperatures_today_second, color="#f8686a", alpha=0.1)
    ax3.set_frame_on(False)
    ax3.plot(times_today_first, temperatures_today_first, color="firebrick", label="Temperatur Außen", linewidth=2.5)
    ax3.plot(times_today_second, temperatures_today_second, color="#f8686a", label="Temperatur Korridor", linestyle="--", linewidth=2.5)
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
    #ax2.fill_between(times_second, humidity_second, color="teal", alpha=0.1)
    ax2.set_frame_on(False)
    ax2.plot(times, humidity, label="Luftfeuchte 1", linewidth=2.5)
    #ax2.plot(times_second, humidity_second, color="teal", label="Luftfeuchte 2", linestyle="--", linewidth=2.5)
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
    ax4.plot(times_today_first, humidityToday, label="Luftfeuchte 1", linewidth=2.5)
    #ax4.plot(times_today_second, humidity_today_second, color="teal", label="Luftfeuchte 2", linestyle="--", linewidth=2.5)
    legend = ax4.legend(fontsize=16)
    legend.get_frame().set_facecolor("#F0F8FF")
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    #fig4.patch.set_facecolor('#F0F8FF')
    #ax4.set_facecolor('#F0F8FF')
    figure = FigureCanvasTkAgg(fig4, master=graph_frame)
    return figure, ax4, fig4


def read_file():
    generalInformation = "TODO"
    textInformation.delete("1.0", tk.END)
    textInformation.insert(tk.END, generalInformation)
    textInformation.tag_configure("left_align", justify="left")
    textInformation.tag_add("left_align", "1.0", tk.END)



# Date Information
today_date = datetime.today()
date_last_week = today_date + timedelta(days=-7)

print(today_date)
print(today_date.strftime('%Y-%m-%d'))
print(date_last_week.strftime('%Y-%m-%d'))

FileManagement.create_csv(datetime.today().date())
# Current Request
#urlCurrent = "https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/current/288"
#dataCurrent = requests.get(urlCurrent).json()

# Data Request Station 288
#url = f"https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/historic/288/{date_last_week.strftime('%Y-%m-%d')}/{today_date.strftime('%Y-%m-%d')}"
#data = requests.get(url).json()

# Data Request Station 287
#urlSecond = f"https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/historic/287/{date_last_week.strftime('%Y-%m-%d')}/{today_date.strftime('%Y-%m-%d')}"
#dataSecond = requests.get(url).json()

utci = None

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

#Get Font
font_family = "Ubuntu Bold"
font_size = 48
custom_font = font.Font(family=font_family, size=font_size)

# Left Frame
text_frame = tk.Frame(root, bg="white")
text_frame.pack(side="left", fill="both", expand=True)

# Frame MP4
videoFrame = tk.Frame(text_frame, bg="#F0F8FF")
videoFrame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# Header "Visualisierungen zu Planung und Fertigung"
header_visualization = tk.Label(videoFrame, text='Visualisierungen zu Planung und Fertigung', justify="left", font=custom_font, bg='#F0F8FF', fg='black')
header_visualization.pack(side="top", padx=10, pady=10)

# Video
my_label = tk.Label(videoFrame, justify="left")
my_label.pack()

player = tkvideo("/home/buga/wetter-screen/pictures/sample.mp4", my_label, loop=1, size=(1280, 720))
player.play()

# Frame Information
informationFrame = tk.Frame(text_frame, bg="#F0F8FF")
informationFrame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# Header "Allgemeine Informationen"
header_information = tk.Label(informationFrame, text='Allgemeine Informationen', justify="left", font=custom_font, bg='#F0F8FF', fg='black')
header_information.pack(side="top", padx=10, pady=10)

information = "Für Fragen und Informationen werden an folgenden Tagen Mitarbeiter des ReGrow Projektes zur Verfügung stehen:\n- 22.06. (Fokus:Mikroklima)\n- .."

textInformation = tk.Text(informationFrame, font=("Arial", 24), bg='#F0F8FF', fg='black', height=10, width=80, borderwidth=0, highlightthickness=0)
textInformation.pack(side="top")
textInformation.insert("1.0", information, "left")
read_file()

######################################

# Right Frame
rightFrame = tk.Frame(root, bg="white")
rightFrame.pack(side="right", fill="both", expand=True)


# Right-Left Frame
graph_frame = tk.Frame(rightFrame, bg="white")
graph_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Value Format
date_format = '%Y-%m-%dT%H:%M:%SZ'

currentTime = datetime.today()
currentTemperatureOutside = SensorInformation.getTemperatureOutside()
currentTemperatureCorridor = SensorInformation.getTemperatureCorridor()

# Values of Temperatures
times_today_first = [currentTime]
times_today_second = [currentTime]
temperatures_today_first = [currentTemperatureOutside]
#times_today_second = []
temperatures_today_second = [currentTemperatureCorridor]
#humidityToday = []
#humidity_today_second = []
times = [currentTime]
times_second = [currentTime]
#timesMatplotlib = []
#times_matplotlib_second = []
#humidity = []
#humidity_second = []
temperatures = [currentTemperatureOutside]
temperatures_second = [currentTemperatureCorridor]
minutesOverThirty = 0

#delta = timedelta(hours=2)

#for element in data["data"]:
#    rightTime = datetime.strptime(str(element), date_format) + delta
#    times.append(rightTime)
#    temperatures.append(float(data["data"][element]["t2m_med"]))
#    if (float(data["data"][element]["t2m_med"]) > 30):
#        minutesOverThirty += 1
#    if rightTime >= (datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)):
#        times_today_first.append(rightTime)
#        temperatures_today_first.append(float(data["data"][element]["t2m_med"]))
#        humidityToday.append(float(data["data"][element]["rf_med"]))
#    humidity.append(float(data["data"][element]["rf_med"]))

#for element in dataSecond["data"]:
#    rightTime = datetime.strptime(str(element), date_format) + delta
#    times_second.append(rightTime)
#    temperatures_second.append(float(dataSecond["data"][element]["t2m_med"]) + 5)
#    if (float(data["data"][element]["t2m_med"]) > 30):
#        minutesOverThirty += 1
#    if rightTime >= (datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)):
#        times_today_second.append(rightTime)
#        temperatures_today_second.append(float(dataSecond["data"][element]["t2m_med"]) + 5)
#        humidity_today_second.append(float(dataSecond["data"][element]["rf_med"]) - 5)
#    humidity_second.append(float(dataSecond["data"][element]["rf_med"]) - 5)

#currentTemperature = temperatures[len(temperatures) - 1]
#test = datetime.strptime(str(times[len(times) - 1]), date_format)
#currentTime = (times[len(times) - 1])
#print(currentTime)
#if(currentTime < (datetime.now() - timedelta(minutes=40))):
#    currentTemperature = "--"
#    utci = "--"


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
#humidityGraphDay = createHumidityGraphDay()
#humidityGraphWeek = createHumidityGraphWeek()

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
