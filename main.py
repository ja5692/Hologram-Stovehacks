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
    #Log temperature
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    temperature = '{0:0.1f}'.format(temperature)
    humidity = '{0:0.1f}'.format(humidity)
    print "humid:"
    print humidity
    print "temp:"
    print temperature

    #Upload Data
    hologram.sendMessage(json.dumps({"Humidity":Humidity, "Temperature":temperature}))

update()
hologram.network.disconnect()
