from Hologram.HologramCloud import HologramCloud
import json
import threading
import time
import sys
import Adafruit_DHT

#Instantiating a hologram instance
hologram = HologramCloud(dict(), network='cellular')

result = hologram.network.connect()
if result == False:
    print ' Failed to connect to cell network'

def update():
    #Find Location
    location = hologram.network.location
    print "Altitude:"
    print location.altitude
    print "Longitude:"
    print location.longitude
    print "Latitude:"
    print location.latitude
    print "Uncertainty:"
    print location.uncertainty
    print "Date:"
    print location.date
    print "Time:"
    print location.time

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    print "temp:"+temperature
    print "humid:"+humidity

    #Upload Databa
    hologram.sendMessage(json.dumps({"Altitude":location.altitude, "Longitude":location.longitude, "Latitude":location.latitude, "Uncertainty": location.uncertainty, "Date":location.date, "Time":location.time}))

update()
hologram.network.disconnect()
