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

def update():
    #Log temperature
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    temperature = '{0:0.1f}'.format(temperature)

    #Determine if stove is on or off
    if temperature <= 30:
        hologram.sendMessage(json.dumps("Your stove is off." + "Temperature: " + temperature + "C"))
        print "Your stove is off." + "Temperature: " + temperature + "C"
    else:
        hologram.sendMessage(json.dumps("Your stove is on. Would you like it to be turned off?" + "Temperature: " + temperature + "C"))
        print "Your stove is on. Would you like it to be turned off?" + "Temperature: " + temperature + "C"
        #User replies
        #Process response and act accordingly

#User asks for status
while True:
    sms_obj = hologram.popReceivedSMS()
    if sms_obj is not None:
        hologram.sendMessage(json.dumps("Message:" + sms_obj["message"]))
        print "Message:" + sms_obj["message"]
        update()
        break
    time.sleep(1)

hologram.network.disconnect()
