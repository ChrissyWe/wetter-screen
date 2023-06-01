import tkinter as tk
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkvideo import tkvideo
import requests
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import UTCI

def updateGUI():
    print("test")
    utci = 3
    print("new value")
def repeatUpdate():
    updateGUI()
    root.after(60000, repeatUpdate())

def toggleGraphs():
    global currentGraphTemperature
    global currentGraphHumidity
    global counter

    if currentGraphTemperature is not None:
        currentGraphTemperature.get_tk_widget().destroy()

    if currentGraphHumidity is not None:
        currentGraphHumidity.get_tk_widget().destroy()

    if counter == 0:
        currentGraphTemperature = createTemperatureGraphWeek()
        currentGraphHumidity = createHumidityGraphWeek()
        counter = 1
    else:
        currentGraphTemperature = createTemperatureGraphDay()
        currentGraphHumidity = createHumidityGraphDay()
        counter = 0

    currentGraphTemperature.get_tk_widget().pack(side="top", fill="both", expand=True)
    currentGraphHumidity.get_tk_widget().pack(sid="top", fill="both", expand=True)

    root.after(5000, toggleGraphs)

def createTemperatureGraphWeek():
    # Graph 1 (Temperature - Week)
    fig1, ax1 = plt.subplots()
    ax1.set_title('Temperaturen der letzten Woche', color="black")
    ax1.set_ylabel("Temperatur")
    ax1.tick_params(colors="black")
    for spine in ax1.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax1.fill_between((datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0), currentTime), 0,
                     30, facecolor='orange', alpha=0.2)
    # ax1.fill_between(x, y2, color="green", label='Temperatur Korridor 1', alpha=0.3)
    # ax1_legend = ax1.legend(loc='upper right')
    # ax1_legend.get_frame().set_facecolor('#191919')
    # ax1_legend.get_texts()[0].set_color('white')
    # ax1_legend.get_texts()[1].set_color('white')
    ax1.set_frame_on(False)
    ax1.plot(times, temperatures, color="red", label="Sinus")
    # ax1.fill_between( , facecolor='orange')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    # ax1.plot(x, y2, color="green")
    fig1.patch.set_facecolor('#F0F8FF')
    ax1.set_facecolor('#F0F8FF')
    return FigureCanvasTkAgg(fig1, master=graph_frame)
    # temperatureGraphWeek.draw()
    # temperatureGraphWeek.get_tk_widget().pack(side="top", fill="both", expand=True)

def createTemperatureGraphDay():
    # Graph 1 (Temperature - Day)
    fig3, ax3 = plt.subplots()
    ax3.set_title('Temperaturen heute', color="black")
    ax3.set_ylabel("Temperatur")
    ax3.tick_params(colors="black")
    for spine in ax3.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax3.set_frame_on(False)
    ax3.plot(timesToday, temperaturesToday, color="red")
    fig3.patch.set_facecolor('#F0F8FF')
    return FigureCanvasTkAgg(fig3, master=graph_frame)

def createHumidityGraphWeek():
    # Graph 2 (Humidity)
    fig2, ax2 = plt.subplots()
    ax2.set_title('Relative Luftfeuchte der letzten Woche', color="black")
    ax2.set_ylabel("Luftfeuchte", color="black")
    ax2.tick_params(colors="black")
    for spine in ax2.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax2.fill_between((datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0), currentTime), 0,
                     100, facecolor='orange', alpha=0.2)
    ax2.set_frame_on(False)
    ax2.plot(times, humidity)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    fig2.patch.set_facecolor('#F0F8FF')
    ax2.set_facecolor('#F0F8FF')
    #canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
    #canvas2.draw()
    #canvas2.get_tk_widget().pack(side="top", fill="both", expand=True)
    return FigureCanvasTkAgg(fig2, master=graph_frame)

def createHumidityGraphDay():
    # Graph 2 (Humidity)
    fig4, ax4 = plt.subplots()
    ax4.set_title('Relative Luftfeuchte der letzten Woche', color="black")
    ax4.set_ylabel("Luftfeuchte", color="black")
    ax4.tick_params(colors="black")
    for spine in ax4.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(1)
    ax4.set_frame_on(False)
    ax4.plot(timesToday, humidityToday)
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    fig4.patch.set_facecolor('#F0F8FF')
    ax4.set_facecolor('#F0F8FF')
    return FigureCanvasTkAgg(fig4, master=graph_frame)

# Date Information
today_date = datetime.today()
date_last_week = today_date + timedelta(days=-7)

print(today_date)
print(today_date.strftime('%Y-%m-%d'))
print(date_last_week.strftime('%Y-%m-%d'))

# Current Request
urlCurrent = "https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/current/288"
dataCurrent = requests.get(urlCurrent).json()

# Data Request
url = f"https://stadtklimaanalyse-mannheim.de/wp-json/climate-data/v1/historic/288/{date_last_week.strftime('%Y-%m-%d')}/{today_date.strftime('%Y-%m-%d')}"
data = requests.get(url).json()

# Calculate UTCI
utci = round(UTCI.universal_thermal_climate_index(float(dataCurrent["t2m_med"]), float(dataCurrent["t2m_med"]), float(dataCurrent["wg_med"]), float(dataCurrent["rf_med"])), 1)

# Main-Window
root = tk.Tk()
root.config(background="white")

#root.attributes("-fullscreen", True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#root.geometry(f"{screen_width}x{screen_height}")

left_width_pct = 0.5
right_width_pct = 1.0 - left_width_pct

#Get Font
font_family = "Ubuntu Bold"
font_size = 24
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
player = tkvideo("C:\\Users\\Chris\\Documents\\Semester_8\\Bundesgartenschau\\sample.mp4", my_label, loop=1, size=(864, 486))
player.play()

# Frame Information
informationFrame = tk.Frame(text_frame, bg="#F0F8FF")
informationFrame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# Header "Allgemeine Informationen"
header_information = tk.Label(informationFrame, text='Allgemeine Informationen', justify="left", font=custom_font, bg='#F0F8FF', fg='black')
header_information.pack(side="top", padx=10, pady=10)

# Text Information
information = "Für Fragen und Informationen werden an folgenden Tagen Mitarbeiter des ReGrow Projektes zur Verfügung stehen:\n- 22.06. (Fokus:Mikroklima)\n- .."

text_information = tk.Label(informationFrame, text=information, justify="left", font=("Arial", 12), bg='#F0F8FF', fg='black')
text_information.pack(side="top", padx=10, pady=10)

######################################

# Right Frame
rightFrame = tk.Frame(root, bg="white")
rightFrame.pack(side="right", fill="both", expand=True)


# Right-Left Frame
graph_frame = tk.Frame(rightFrame, bg="#F0F8FF")
graph_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Value Format
date_format = '%Y-%m-%dT%H:%M:%SZ'

# Values of Temperatures
timesToday = []
temperaturesToday =[]
humidityToday = []
times = []
timesMatplotlib = []
humidity = []
temperatures = []

delta = timedelta(hours=2)

for element in data["data"]:
    rightTime = datetime.strptime(str(element), date_format) + delta
    times.append(rightTime)
    temperatures.append(float(data["data"][element]["t2m_med"]))
    if rightTime >= (datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)):
        timesToday.append(rightTime)
        temperaturesToday.append(float(data["data"][element]["t2m_med"]))
        humidityToday.append(float(data["data"][element]["rf_med"]))
    humidity.append(float(data["data"][element]["rf_med"]))

currentTemperature = temperatures[len(temperatures) - 1]
#test = datetime.strptime(str(times[len(times) - 1]), date_format)
currentTime = (times[len(times) - 1])
print(currentTime)
if(currentTime < (datetime.now() - timedelta(minutes=40))):
    currentTemperature = "--"
    utci = "--"
#print(times)
#print(timesMatplotlib)
#print(temperatures)
#print(humidity)

# Header "Informationen zum Mikroklima dieses Pavillions"
header_climate = tk.Label(graph_frame, text='Informationen zum Mikroklima dieses Pavillons', font=custom_font, bg='#F0F8FF', fg='black', anchor="w")
header_climate.pack(side="top", padx=10, pady=10)

#Right Frame Information
#graph_frame_text = tk.Frame(graph_frame)
#graph_frame_text.pack(side="left")

# Frame for Temperature
#temperature_frame = tk.Frame(graph_frame)
#temperature_frame.pack(side="right", fill="both", expand=True)

#Frame for Information
informationGraphs = tk.Frame(graph_frame, bg='#F0F8FF')
informationGraphs.pack(side="top")

#Right Frame for Temperature Information
informationTemperature = tk.Frame(informationGraphs)
informationTemperature.pack(side="left",padx=10,pady=10)

#Left Frame for Humidity Information
informationHumidity = tk.Frame(informationGraphs)
informationHumidity.pack(side="right",padx=10,pady=10)

# Text above Graph
current = f"Aktuelle Temperatur außen: {currentTemperature} °C\nAktuelle Temperatur in Sprühanlage 1: {currentTemperature} °C"

text_temperatures = tk.Text(informationTemperature, font=("Arial", 12), bg='#F0F8FF', fg='black', height=2, width=50, borderwidth=0)
text_temperatures.pack(side="top")
text_temperatures.insert("1.0", current)


start_index = text_temperatures.search(str(currentTemperature) + " °C", "1.0", stopindex=tk.END)
second_occurrence_index = text_temperatures.search(str(currentTemperature), f"{start_index}+1c", stopindex=tk.END)
end_index = f"{start_index}+{len(str(currentTemperature)) + 3}c"
text_temperatures.tag_configure("blue", foreground="blue", font=("Arial", 12, "bold"))
text_temperatures.tag_add("blue", start_index, end_index)

text_temperatures.tag_configure("blue", foreground="blue", font=("Arial", 12, "bold"))
text_temperatures.tag_add("blue", second_occurrence_index, f"{second_occurrence_index}+{len(str(currentTemperature)) + 3}c")

heatWithoutSystem = 0.0
heatWithSystem = 0.0

# Text beside Humidity
humidity_information = f"Stunden über 30°C bis jetzt außen, ohne Sprühanlage: {heatWithoutSystem}\nStunden über 30°C bis jetzt mit Sprühanlage: {heatWithSystem}"

text_humidity_information = tk.Text(informationHumidity, font=("Arial", 12), bg='#F0F8FF', fg='black', height=2, width=50, borderwidth=0)
text_humidity_information.pack(side="top")
text_humidity_information.insert("1.0", humidity_information)

startIndexHumidity = text_humidity_information.search(str(heatWithoutSystem), "1.0", stopindex=tk.END)
secondIndexHumidity = text_humidity_information.search(str(heatWithSystem), f"{startIndexHumidity}+1c", stopindex=tk.END)
endIndexHumidity = f"{startIndexHumidity}+{len(str(heatWithoutSystem))}c"
secondEndHumidity = f"{secondIndexHumidity}+{len(str(heatWithSystem))}c"
text_humidity_information.tag_configure("blue", foreground="blue", font=("Arial", 12, "bold"))
text_humidity_information.tag_add("blue", secondIndexHumidity, secondEndHumidity)
text_humidity_information.tag_add("blue", startIndexHumidity, endIndexHumidity)



# Values of Graph 1
x = np.linspace(0, 1, 10)
y1 = np.cos(x)
y2 = np.sin(x)

counter = 0
temperatureGraphDay = createTemperatureGraphDay()
temperatureGraphWeek = createTemperatureGraphWeek()
humidityGraphDay = createHumidityGraphDay()
humidityGraphWeek = createHumidityGraphWeek()

currentGraphHumidity = None
currentGraphTemperature = None
toggleGraphs()


#TODO: Clear plots maybe

# UTCI Calculator
UTCIFrame = tk.Frame(rightFrame, bg="#F0F8FF")
UTCIFrame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# UTCI Information
currentUTCI = f"Gefühlte Außenluft-\nTemperatur Aktuell: \n {utci} °C"

textUTCI = tk.Text(UTCIFrame, font=("Arial", 12), bg='#F0F8FF', fg='black', height=3, width=20, borderwidth=0)
textUTCI.insert("1.0", currentUTCI, "center")
textUTCI.tag_configure("center", justify="center")
textUTCI.tag_add("center", "1.0", "end")
textUTCI.pack(side="top")

# Makes the Temperature blue
startIndexUTCI = textUTCI.search(str(utci) + " °C", "1.0", stopindex=tk.END)
endIndexUTCI = f"{startIndexUTCI}+{len(str(utci)) + 3}c"
textUTCI.tag_configure("blue", foreground="blue", font=("Arial", 12, "bold"))
textUTCI.tag_add("blue", startIndexUTCI, endIndexUTCI)

# Canvas, width normally 264
canvas = tk.Canvas(UTCIFrame, width=int((264/2)+10+45), height=int((1753/2)+20), bg='#F0F8FF')
canvas.pack(side="top")

# Load Image
UTCIImage = tk.PhotoImage(file="C:\\Users\\Chris\\Documents\\Semester_8\\Bundesgartenschau\\UTCI-Chart.png")
UTCIImage = UTCIImage.subsample(2) #Resize 1/2
canvas.create_image(45, 10, anchor="nw", image=UTCIImage)

# Draw Arrow with Text
UTCIArrow = tk.PhotoImage(file="C:\\Users\\Chris\\Documents\\Semester_8\\Bundesgartenschau\\UTCI-Arrow.png")
UTCIArrow = UTCIArrow.subsample(2)
if utci == "--":
    utci = ""
elif utci <= 0:
    canvas.create_image(5, 555, anchor="nw", image=UTCIArrow)
elif utci <= 9:
    canvas.create_image(5, 470, anchor="nw", image=UTCIArrow)
elif utci <= 26:
    canvas.create_image(5, 380, anchor="nw", image=UTCIArrow)
elif utci <= 32:
    canvas.create_image(5, 290, anchor="nw", image=UTCIArrow)
elif utci <= 38:
    canvas.create_image(5, 210, anchor="nw", image=UTCIArrow)

# UTCI = Universal Thermal Climate Index
currentUTCI = f"(UTCI - Universal \nThermal Climate Index)"

textUTCI = tk.Text(UTCIFrame, font=("Arial", 8), bg='#F0F8FF', fg='black', height=3, width=20, borderwidth=0)
textUTCI.insert("1.0", currentUTCI, "center")
textUTCI.tag_configure("center", justify="center")
textUTCI.tag_add("center", "1.0", "end")
textUTCI.pack(side="top")

#updateGUI()

# Main loop
root.mainloop()
