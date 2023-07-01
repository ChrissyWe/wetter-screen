import time

import pandas as pd
from datetime import datetime, timedelta

def create_csv():
    csv = pd.DataFrame(columns = ["Uhrzeit", "Temperatur_aussen", "Temperatur_spruehanlage", "ueber_30_C"])
    csv.to_csv(f"/wetter-screen/Data/{datetime.today().date()}_Temperatures.csv", sep=";", index = False)
    #csv.to_csv(f"/wetter-screen/Data/Temperatur_{datum}.csv", sep = ";")

def import_values_to_csv(time, temperatureOutside, temperatureCorridor, above30):
    dataframe = pd.read_csv(f"/wetter-screen/Data/{datetime.today().date()}_Temperatures.csv", sep = ";")
    act_index = dataframe.index.max() + 1
    dataframe.loc[act_index, "Uhrzeit"] = time
    dataframe.loc[act_index, "Temperatur_aussen"] = temperatureOutside
    dataframe.loc[act_index, "Temperatur_spruehanlage"] = temperatureCorridor
    dataframe.loc[act_index, "ueber_30_C"] = above30
    dataframe.to_csv(f"/wetter-screen/Data/{datetime.today().date()}_Temperatures.csv",  sep=";", index = False)


