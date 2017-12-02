from Hologram.HologramCloud import HologramCloud
import json
import threading

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

    #Upload Databa
    hologram.sendMessage(json.dumps({"Altitude":location.altitude, "Longitude":location.longitude, "Latitude":location.latitude, "Uncertainty": location.uncertainty, "Date":location.date, "Time":location.time}))

t = Timer(600.0, update)
t.start()

#End connection when user presses "ESC"
while True:
    key = ord(getch())
    if key == 27:
        t.cancel()
        #Disconnect
        hologram.network.disconnect()
