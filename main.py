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
utci = UTCI.universal_thermal_climate_index(float(dataCurrent["t2m_med"]), float(dataCurrent["gs_med"]), float(dataCurrent["wg_med"]), float(dataCurrent["rf_med"]))

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
player = tkvideo("home/buga/wetter-screen/pictures/sample.mp4", my_label, loop=1, size=(864,486))
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
times = []
timesMatplotlib = []
humidity = []
temperatures = []

for element in data["data"]:
    times.append(element)
    temperatures.append(float(data["data"][element]["t2m_med"]))
    timesMatplotlib.append(dt.datetime.strptime(element, date_format))
    humidity.append(float(data["data"][element]["rf_med"]))

currentTemperature = temperatures[len(temperatures) - 1]
print(times)
#print(timesMatplotlib)
print(temperatures)
print(humidity)

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

# Text beside Humidity
humidity_information ="Stunden über 30°C bis jetzt außen, ohne Sprühanlage: 12\nStunden über 30°C bis jetzt mit Sprühanlage: 2"

text_humidity_information = tk.Label(informationHumidity, text=humidity_information, bg="#F0F8FF", justify="left", font=("Arial", 12))
text_humidity_information.pack(side="top")



# Values of Graph 1
x = np.linspace(0, 1, 10)
y1 = np.cos(x)
y2 = np.sin(x)

# Graph 1 (Temperature)
fig1, ax1 = plt.subplots()
ax1.set_title('Temperaturen der letzten Woche', color="black")
ax1.set_ylabel("Temperatur")
ax1.tick_params(colors="black")
for spine in ax1.spines.values():
    spine.set_edgecolor("black")
    spine.set_linewidth(1)
#ax1.fill_between(timesMatplotlib, temperatures, color="red", label='Temperatur außerhalb', alpha=0.3)
#ax1.fill_between(x, y2, color="green", label='Temperatur Korridor 1', alpha=0.3)
#ax1_legend = ax1.legend(loc='upper right')
#ax1_legend.get_frame().set_facecolor('#191919')
#ax1_legend.get_texts()[0].set_color('white')
#ax1_legend.get_texts()[1].set_color('white')
ax1.set_frame_on(False)
ax1.plot(timesMatplotlib, temperatures, color="red", label="Sinus")
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
#ax1.plot(x, y2, color="green")
fig1.patch.set_facecolor('#F0F8FF')
ax1.set_facecolor('#F0F8FF')
canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
canvas1.draw()
canvas1.get_tk_widget().pack(side="top", fill="both", expand=True)

# Graph 2 (Humidity)
fig2, ax2 = plt.subplots()
ax2.set_title('Relative Luftfeuchte der letzten Woche',color="black")
ax2.set_ylabel("Luftfeuchte", color="black")
ax2.tick_params(colors="black")
for spine in ax2.spines.values():
    spine.set_edgecolor("black")
    spine.set_linewidth(1)
ax2.set_frame_on(False)
ax2.plot(timesMatplotlib, humidity)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
fig2.patch.set_facecolor('#F0F8FF')
ax2.set_facecolor('#F0F8FF')
canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
canvas2.draw()
canvas2.get_tk_widget().pack(side="top", fill="both", expand=True)

#TODO: Clear plots maybe

# UTCI Calculator
UTCIFrame = tk.Frame(rightFrame, bg="#F0F8FF")
UTCIFrame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# UTCI Information
currentUTCI = f"Gefühlte Außenluft-\nTemperatur Aktuell: \n {round(utci, 1)} °C"

textUTCI = tk.Text(UTCIFrame, font=("Arial", 12), bg='#F0F8FF', fg='black', height=3, width=20, borderwidth=0)
textUTCI.insert("1.0", currentUTCI, "center")
textUTCI.tag_configure("center", justify="center")
textUTCI.tag_add("center", "1.0", "end")
textUTCI.pack(side="top")

# Makes the Temperature blue
startIndexUTCI = textUTCI.search(str(round(utci, 1)) + " °C", "1.0", stopindex=tk.END)
endIndexUTCI = f"{startIndexUTCI}+{len(str(round(utci, 1))) + 3}c"
textUTCI.tag_configure("blue", foreground="blue", font=("Arial", 12, "bold"))
textUTCI.tag_add("blue", startIndexUTCI, endIndexUTCI)

# Canvas, width normally 264
canvas = tk.Canvas(UTCIFrame, width=int((264/2)+10+45), height=int((1753/2)+20), bg='#F0F8FF')
canvas.pack(side="top")

# Load Image
UTCIImage = tk.PhotoImage(file="home/buga/wetter-screen/pictures/UTCI-Chart.png")
UTCIImage = UTCIImage.subsample(2) #Resize 1/2
canvas.create_image(45, 10, anchor="nw", image=UTCIImage)

# Draw Arrow with Text
UTCIArrow = tk.PhotoImage(file="home/buga/wetter-screen/pictures/UTCI-Arrow.png")
UTCIArrow = UTCIArrow.subsample(2)
if utci <= 0:
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

# Main loop
root.mainloop()
