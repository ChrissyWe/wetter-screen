#!/usr/bin/python
# misst Temperaturen mit DS1820
import time

def getTemperature():
    tempfile = open("/sys/bus/w1/devices/28-3ce104577a04/w1_slave")
    content = tempfile.read()
    tempfile.close()
    tempdata = content.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:])
    temperature = temperature/1000
    #print("Temperatur betraegt: " + str(temperature) + " Grad")
    return temperature