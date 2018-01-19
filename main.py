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
    print "Variable type: " + type(temperature)

    #Determine if stove is on or off
    if temperature <= 30:
        #hologram.sendMessage(json.dumps("Your stove is off." + "Temperature: " + temperature + "C"))
        print "Your stove is off." + "Temperature: " + temperature + "C"
    else:
        #hologram.sendMessage(json.dumps("Your stove is on. Would you like it to be turned off?" + "Temperature: " + temperature + "C"))
        print "Your stove is on. Would you like it to be turned off?" + "Temperature: " + temperature + "C"

        count = 0
        while True:
            sms_obj = hologram.popReceivedSMS()
            message = sms_obj.message
            if message == "yes":
                #hologram.sendMessage(json.dumps("Turning off stove."))
                print "Turning off stove."
                break
            elif message == "no":
                #hologram.sendMessage(json.dumps("Ok. Stove will be left on."))
                print "Ok. Stove will be left on."
                break
            elif message:
                #hologram.sendMessage(json.dumps("Please enter a valid response. (yes/no)"))
                print "Please enter a valid response. (yes/no)"
            elif count >= 30:
                #hologram.sendMessage(json.dumps("Message: " + message))
                print "No response recieved within 30 minutes. Reverting to standby."
                break
            count += 1
            time.sleep(1)

#User asks for status
while True:
    sms_obj = hologram.popReceivedSMS()
    message = sms_obj.message

    if message == "status":
        #hologram.sendMessage(json.dumps("Message: " + message))
        print "Message: " + message
        update()
        break
    time.sleep(1)

hologram.network.disconnect()
