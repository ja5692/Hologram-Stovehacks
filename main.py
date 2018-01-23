from Hologram.HologramCloud import HologramCloud
import json
import threading
import time
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO

mintemp = 30 #Minimum temperature required to trigger the "stove on" status
sensor = Adafruit_DHT.DHT11 #Sensor type. Change to Adafruit_DHT.DHT22 if using a DHT 22 sensor.
GPIO.setmode(GPIO.BOARD)
dhtpin = 7 #GPIO pin the DHT is connected to
servopin = 11 #GPIO pin the servo motor is connected to
GPIO.setup(servopin,GPIO.OUT)

#Starts servo in neutral position
servo = GPIO.PWM(11, 50)
servo.start(7.5)

#Instantiating a hologram instance
hologram = HologramCloud(dict(), network='cellular')

result = hologram.network.connect()
print 'CONNECTION STATUS: ' + str(hologram.network.getConnectionStatus())

if result == False:
    print ' Failed to connect to cell network'
else:
    print "Connection successful!"
    print "Hologram online!"
    #Enables Hologram to listen for incoming SMS messages
    recv = hologram.enableSMS()

def update():
    #Log temperature
    humidity, temperature = Adafruit_DHT.read_retry(sensor, dhtpin)
    temperature = float('{0:0.1f}'.format(temperature))
    print "Variable type: " + str(type(temperature))

    #Determine if stove is on or off
    if temperature <= mintemp:
        #hologram.sendMessage(json.dumps("Your stove is off." + "Temperature: " + temperature + "C"))
        print "Your stove is off. " + "Temperature: " + str(temperature) + "C"
    else:
        #hologram.sendMessage(json.dumps("Your stove is on. Would you like it to be turned off?" + "Temperature: " + temperature + "C"))
        print "Your stove is on. Would you like it to be turned off?" + "Temperature: " + str(temperature) + "C"
        #Waits for and processes user response to prompt
        count = 0
        while True:
            #Reads user response
            sms_obj = hologram.popReceivedSMS()
            if sms_obj is not None:
                message = sms_obj.message.lower()
                if message == "yes":
                    #hologram.sendMessage(json.dumps("Turning off stove."))
                    print "Turning off stove."
                    servo.ChangeDutyCycle(2.5)#Servo turns off stove
                    break
                elif message == "no":
                    #hologram.sendMessage(json.dumps("Ok. Stove will be left on."))
                    print "Ok. Stove will be left on."
                    break
                elif message:
                    #hologram.sendMessage(json.dumps("Please enter a valid response. (yes/no)"))
                    print "Please enter a valid response. (yes/no)"
                    count = 0
                elif count >= 30:
                    #hologram.sendMessage(json.dumps("No response recieved within 30 minutes. Reverting to standby mode."))
                    print "No response recieved within 30 seconds. Reverting to standby mode."
                    break
            count += 1
            time.sleep(1)

#Hologram waits for user input (standby mode)
while True:
    sms_obj = hologram.popReceivedSMS()
    if sms_obj is not None: #If user sends something:
        message = sms_obj.message
        print "Message: " + message

        if message.lower() in "status update": #If user enters keyword
            #hologram.sendMessage(json.dumps("Message: " + message))
            update()
    time.sleep(1)

hologram.network.disconnect()
