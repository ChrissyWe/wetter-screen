#!/usr/bin/python
# misst Temperaturen mit DS1820
import time

""" This class fetches the sensor information. 
To do this, you must first follow this tutorial: 
https://cbrell.de/blog/raspilab-wetterstation-dritte-mission-temperatur-messen-mit-dem-bs18b20/"""


# First Sensor (initially with the grey Jumper Cable)
def getTemperatureOutside():
    #time.sleep(2)
    tempfile = open("/sys/bus/w1/devices/28-3ce10457fddc/w1_slave")
    #tempfile = open("/sys/bus/w1/devices/28-3ce104577a04/w1_slave")
    content = tempfile.read()
    tempfile.close()
    tempdata = content.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:])
    temperature = temperature/1000
    #print("Temperatur betraegt: " + str(temperature) + " Grad")
    return temperature

# Second Sensor (initially with the orange Jumper Cable)
def getTemperatureCorridor():
    #time.sleep(2)
    tempfile = open("/sys/bus/w1/devices/28-3ce104571868/w1_slave")
    #tempfile = open("/sys/bus/w1/devices/28-3ce10457cf88/w1_slave")
    content = tempfile.read()
    tempfile.close()
    tempdata = content.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:])
    temperature = temperature / 1000
    # print("Temperatur betraegt: " + str(temperature) + " Grad")
    return temperature