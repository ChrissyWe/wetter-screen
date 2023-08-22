import time

import pandas as pd
from datetime import datetime, timedelta
import os
import smtplib
import mimetypes
from email.message import EmailMessage

def create_csv(date):
    if(os.path.exists(f"/home/buga/Data/{date}_Temperatures.csv")):
        return
    else:
        csv = pd.DataFrame(columns = ["Uhrzeit", "Temperatur_20m", "Temperatur_15m", "ueber_30_C"])
        csv.to_csv(f"/home/buga/Data/{date}_Temperatures.csv", sep=";", index = False)
    #csv.to_csv(f"/wetter-screen/Data/Temperatur_{datum}.csv", sep = ";")

def import_values_to_csv(time, temperatureOutside, temperatureCorridor, above30):
    if ((os.path.exists(f"/home/buga/Data/{datetime.today().date()}_Temperatures.csv"))):
        now = datetime.now()
        dataframe = pd.read_csv(f"/home/buga/Data/{datetime.today().date()}_Temperatures.csv", sep = ";")
        act_index = dataframe.index.max() + 1
        dataframe.loc[act_index, "Uhrzeit"] = time
        dataframe.loc[act_index, "Temperatur_20m"] = temperatureOutside
        dataframe.loc[act_index, "Temperatur_15m"] = temperatureCorridor
        dataframe.loc[act_index, "ueber_30_C"] = above30
        dataframe.to_csv(f"/home/buga/Data/{datetime.today().date()}_Temperatures.csv",  sep=";", index = False)
        if (datetime(now.year, now.month, now.day, 23, 59, 0) >= time >= datetime(now.year, now.month, now.day, 23, 58, 0)):
            sendMail()
        elif (datetime(now.year, now.month, now.day, 6, 1, 0) >= time >= datetime(now.year, now.month, now.day, 6, 0, 0)):
            sendMail()
        elif (datetime(now.year, now.month, now.day, 12, 1, 0) >= time >= datetime(now.year, now.month, now.day, 12, 0, 0)):
            sendMail()
    else:
        create_csv(datetime.today().date())


def sendMail():
    msg = EmailMessage()
    msg['Subject'] = 'Diese E-mail enthält einen Anhang'
    msg['From'] = 'buga-sensor@gmx.de'
    msg['To'] = 'buga-sensor@gmx.de'
    msg.set_content(f'Hallo,\nIm Anhang befindet sich die Mail für die Temperaturen von {datetime.today()}.')

    filename = f"/home/buga/Data/{datetime.today().date()}_Temperatures.csv"

    with open(filename, 'rb') as fp:
        file_data = fp.read()
        maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
        msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

    s = smtplib.SMTP('mail.gmx.net', 587)
    s.starttls()
    s.login('buga-sensor@gmx.de', 'qgQ35g94nQmbig')
    s.send_message(msg)
    s.quit()


