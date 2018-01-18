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

recv = hologram.enableSMS()

while True:
    sms_obj = hologram.popReceivedSMS()
    if sms_obj != None
        update()
    delay (1000)


def update():
    #Log temperature
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    temperature = '{0:0.1f}'.format(temperature)

    #Determine if stove is on or off
    if temperature <= 30:
        hologram.sendMessage(json.dumps("Your stove is off."))
    else:
        hologram.sendMessage(json.dumps("Your stove is on. Would you like it to be turned off?"))
        #User replies
        #Process response and act accordingly


    #Upload Data
    hologram.sendMessage(json.dumps({"Temperature":temperature + "C"}))

#User asks for status
update()
hologram.network.disconnect()
