import time

import pandas as pd
from datetime import datetime, timedelta
import os

def create_csv(date):
    if(os.path.exists(f"/home/buga/Data/{date}_Temperatures.csv")):
        return
    else:
        csv = pd.DataFrame(columns = ["Uhrzeit", "Temperatur_20m", "Temperatur_15m", "ueber_30_C"])
        csv.to_csv(f"/home/buga/Data/{date}_Temperatures.csv", sep=";", index = False)
    #csv.to_csv(f"/wetter-screen/Data/Temperatur_{datum}.csv", sep = ";")

def import_values_to_csv(time, temperatureOutside, temperatureCorridor, above30):
    dataframe = pd.read_csv(f"/home/buga/Data/{datetime.today().date()}_Temperatures.csv", sep = ";")
    act_index = dataframe.index.max() + 1
    dataframe.loc[act_index, "Uhrzeit"] = time
    dataframe.loc[act_index, "Temperatur_20m"] = temperatureOutside
    dataframe.loc[act_index, "Temperatur_15m"] = temperatureCorridor
    dataframe.loc[act_index, "ueber_30_C"] = above30
    dataframe.to_csv(f"/home/buga/Data/{datetime.today().date()}_Temperatures.csv",  sep=";", index = False)


